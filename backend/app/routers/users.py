"""Users CRUD (admin). Uses store."""
from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_user, hash_password, require_roles
from app.store import list_users as store_list_users, create_user as store_create_user, get_user_by_id, update_user as store_update_user
from app.models import Role
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
async def list_users(current_user=Depends(require_roles(Role.ADMIN))):
    """List all users (admin only)."""
    users = store_list_users()
    return [UserResponse.model_validate(u) for u in users]


@router.post("", response_model=UserResponse)
async def create_user(
    body: UserCreate,
    current_user=Depends(require_roles(Role.ADMIN)),
):
    """Create user (admin only)."""
    try:
        user = store_create_user(
            email=body.email,
            hashed_password=hash_password(body.password),
            full_name=body.full_name,
            role=body.role.value,
            manager_id=body.manager_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return UserResponse.model_validate(user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user=Depends(get_current_user),
):
    """Get user by id. Employees can only get self; admin can get any."""
    if current_user.id != user_id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not allowed")
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    body: UserUpdate,
    current_user=Depends(require_roles(Role.ADMIN)),
):
    """Update user (admin only)."""
    user = store_update_user(
        user_id,
        full_name=body.full_name,
        role=body.role.value if body.role is not None else None,
        manager_id=body.manager_id,
        is_active=body.is_active,
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)
