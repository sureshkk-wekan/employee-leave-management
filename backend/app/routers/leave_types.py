"""Leave types CRUD (admin) and list. Uses store."""
from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_user, require_roles
from app.store import list_leave_types as store_list, get_leave_type, create_leave_type as store_create, update_leave_type as store_update
from app.models import Role
from app.schemas.leave_type import LeaveTypeCreate, LeaveTypeUpdate, LeaveTypeResponse

router = APIRouter(prefix="/leave-types", tags=["leave-types"])


@router.get("", response_model=list[LeaveTypeResponse])
async def list_leave_types(
    current_user=Depends(get_current_user),
    active_only: bool = True,
):
    """List leave types (all authenticated users)."""
    types = store_list(active_only=active_only)
    return [LeaveTypeResponse.model_validate(t) for t in types]


@router.post("", response_model=LeaveTypeResponse)
async def create_leave_type(
    body: LeaveTypeCreate,
    current_user=Depends(require_roles(Role.ADMIN)),
):
    """Create a leave type (admin only)."""
    try:
        lt = store_create(
            name=body.name,
            code=body.code,
            default_days_per_year=body.default_days_per_year,
            allow_carry_over=body.allow_carry_over,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return LeaveTypeResponse.model_validate(lt)


@router.get("/{leave_type_id}", response_model=LeaveTypeResponse)
async def get_leave_type_route(
    leave_type_id: int,
    current_user=Depends(get_current_user),
):
    """Get one leave type."""
    lt = get_leave_type(leave_type_id)
    if not lt:
        raise HTTPException(status_code=404, detail="Leave type not found")
    return LeaveTypeResponse.model_validate(lt)


@router.patch("/{leave_type_id}", response_model=LeaveTypeResponse)
async def update_leave_type_route(
    leave_type_id: int,
    body: LeaveTypeUpdate,
    current_user=Depends(require_roles(Role.ADMIN)),
):
    """Update leave type (admin only)."""
    lt = store_update(
        leave_type_id,
        name=body.name,
        default_days_per_year=body.default_days_per_year,
        allow_carry_over=body.allow_carry_over,
        is_active=body.is_active,
    )
    if not lt:
        raise HTTPException(status_code=404, detail="Leave type not found")
    return LeaveTypeResponse.model_validate(lt)
