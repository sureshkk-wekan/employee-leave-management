"""Leave balances: list. Uses store."""
from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth import get_current_user, require_roles
from app.store import list_leave_balances as store_list
from app.models import Role
from app.schemas.leave_balance import LeaveBalanceResponse

router = APIRouter(prefix="/leave-balances", tags=["leave-balances"])


@router.get("", response_model=list[LeaveBalanceResponse])
async def list_leave_balances(
    current_user=Depends(get_current_user),
    user_id: int | None = Query(None),
    year: int | None = Query(None),
):
    """List leave balances. Employees see own; admin can pass user_id."""
    target_user_id = current_user.id
    if user_id is not None:
        if current_user.role != Role.ADMIN:
            raise HTTPException(status_code=403, detail="Only admin can view another user's balances")
        target_user_id = user_id
    balances = store_list(target_user_id, year=year)
    return [LeaveBalanceResponse.model_validate(b) for b in balances]
