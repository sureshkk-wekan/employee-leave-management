"""Auth: login (issue JWT), me (current user). Uses store."""
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import create_access_token, verify_password, get_current_user
from app.store import get_user_by_email
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(body: LoginRequest):
    """Authenticate with email/password; returns JWT."""
    user = get_user_by_email(body.email)
    if not user or not verify_password(body.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not user.get("is_active", True):
        raise HTTPException(status_code=401, detail="User inactive")
    token = create_access_token(user["id"], user["email"], user["role"])
    return Token(access_token=token)


@router.get("/me", response_model=UserResponse)
async def me(current_user=Depends(get_current_user)):
    """Return current authenticated user."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        manager_id=current_user.manager_id,
        is_active=current_user.is_active,
    )
