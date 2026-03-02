"""Leave requests: create, list, approve/reject. Uses store."""
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.auth import get_current_user, require_roles
from app.store import (
    get_leave_type,
    get_or_create_balance,
    list_leave_requests as store_list_requests,
    get_leave_request,
    create_leave_request as store_create_request,
    update_leave_request_approve,
    add_used_days,
    log_action,
    get_user_by_id,
)
from app.models import Role, LeaveRequestStatus
from app.schemas.leave_request import LeaveRequestCreate, LeaveRequestResponse, LeaveRequestApproveReject


def _days_between(start: date, end: date) -> int:
    return (end - start).days + 1


def _req_to_response(r: dict) -> LeaveRequestResponse:
    return LeaveRequestResponse(
        id=r["id"],
        user_id=r["user_id"],
        leave_type_id=r["leave_type_id"],
        start_date=date.fromisoformat(r["start_date"]) if isinstance(r["start_date"], str) else r["start_date"],
        end_date=date.fromisoformat(r["end_date"]) if isinstance(r["end_date"], str) else r["end_date"],
        reason=r.get("reason"),
        status=LeaveRequestStatus(r["status"]) if isinstance(r["status"], str) else r["status"],
        approved_by_id=r.get("approved_by_id"),
        approved_at=datetime.fromisoformat(r["approved_at"]) if r.get("approved_at") else None,
        rejection_reason=r.get("rejection_reason"),
        created_at=datetime.fromisoformat(r["created_at"]) if isinstance(r.get("created_at"), str) else r["created_at"],
        updated_at=datetime.fromisoformat(r["updated_at"]) if isinstance(r.get("updated_at"), str) else r["updated_at"],
    )


router = APIRouter(prefix="/leave-requests", tags=["leave-requests"])


@router.post("", response_model=LeaveRequestResponse)
async def create_leave_request(
    body: LeaveRequestCreate,
    current_user=Depends(get_current_user),
):
    """Submit a new leave request (employee)."""
    leave_type = get_leave_type(body.leave_type_id)
    if not leave_type or not leave_type.get("is_active", True):
        raise HTTPException(status_code=400, detail="Invalid or inactive leave type")
    start = body.start_date
    end = body.end_date
    year = start.year
    balance = get_or_create_balance(current_user.id, body.leave_type_id, year)
    available = balance["entitlement_days"] + balance.get("carried_over_days", 0) - balance.get("used_days", 0)
    requested_days = _days_between(start, end)
    if requested_days > available:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient balance: requested {requested_days} days, available {available}",
        )
    req = store_create_request(
        user_id=current_user.id,
        leave_type_id=body.leave_type_id,
        start_date=start,
        end_date=end,
        reason=body.reason,
    )
    log_action("leave_request.created", actor_id=current_user.id, target_type="leave_request", target_id=req["id"], details=body.reason)
    return _req_to_response(req)


@router.get("", response_model=list[LeaveRequestResponse])
async def list_leave_requests(
    current_user=Depends(get_current_user),
    status_filter: LeaveRequestStatus | None = Query(None, alias="status"),
    my_only: bool = True,
):
    """List leave requests. Employees see own; managers/admins can see team/all."""
    role_str = current_user.role.value if hasattr(current_user.role, "value") else current_user.role
    requests = store_list_requests(
        current_user_id=current_user.id,
        current_user_role=role_str,
        my_only=my_only,
        status_filter=status_filter.value if status_filter else None,
    )
    return [_req_to_response(r) for r in requests]


@router.get("/{request_id}", response_model=LeaveRequestResponse)
async def get_leave_request_route(
    request_id: int,
    current_user=Depends(get_current_user),
):
    """Get one leave request (owner or manager/admin)."""
    req = get_leave_request(request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Leave request not found")
    if req["user_id"] != current_user.id and current_user.role not in (Role.MANAGER, Role.ADMIN):
        raise HTTPException(status_code=403, detail="Not allowed to view this request")
    return _req_to_response(req)


@router.post("/{request_id}/approve", response_model=LeaveRequestResponse)
async def approve_or_reject(
    request_id: int,
    body: LeaveRequestApproveReject,
    current_user=Depends(require_roles(Role.MANAGER, Role.ADMIN)),
):
    """Approve or reject a leave request (manager/admin)."""
    req = get_leave_request(request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Leave request not found")
    if req["status"] != "pending":
        raise HTTPException(status_code=400, detail="Request is not pending")
    if current_user.role == Role.MANAGER:
        requestor = get_user_by_id(req["user_id"])
        if not requestor or requestor.get("manager_id") != current_user.id:
            raise HTTPException(status_code=403, detail="You can only approve your reportees")
    update_leave_request_approve(
        request_id,
        approved=body.approved,
        approved_by_id=current_user.id,
        rejection_reason=body.rejection_reason,
    )
    if body.approved:
        start = date.fromisoformat(req["start_date"]) if isinstance(req["start_date"], str) else req["start_date"]
        end = date.fromisoformat(req["end_date"]) if isinstance(req["end_date"], str) else req["end_date"]
        add_used_days(req["user_id"], req["leave_type_id"], start.year, _days_between(start, end))
    log_action(
        "leave_request.approved" if body.approved else "leave_request.rejected",
        actor_id=current_user.id,
        target_type="leave_request",
        target_id=request_id,
        details=body.rejection_reason,
    )
    req = get_leave_request(request_id)
    return _req_to_response(req)
