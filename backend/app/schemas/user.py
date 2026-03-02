"""User schemas."""
from pydantic import BaseModel
from app.models import Role


class UserBase(BaseModel):
    """Shared fields."""

    email: str
    full_name: str
    role: Role
    manager_id: int | None = None


class UserCreate(UserBase):
    """Create user (password required)."""

    password: str


class UserUpdate(BaseModel):
    """Partial update."""

    full_name: str | None = None
    role: Role | None = None
    manager_id: int | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    """User in API responses (no password)."""

    id: int
    is_active: bool

    class Config:
        from_attributes = True
