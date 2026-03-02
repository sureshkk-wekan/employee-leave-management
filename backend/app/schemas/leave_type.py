"""Leave type schemas."""
from pydantic import BaseModel


class LeaveTypeBase(BaseModel):
    """Shared fields."""

    name: str
    code: str
    default_days_per_year: int = 0
    allow_carry_over: bool = False


class LeaveTypeCreate(LeaveTypeBase):
    """Create leave type."""

    pass


class LeaveTypeUpdate(BaseModel):
    """Partial update."""

    name: str | None = None
    default_days_per_year: int | None = None
    allow_carry_over: bool | None = None
    is_active: bool | None = None


class LeaveTypeResponse(LeaveTypeBase):
    """Leave type in API responses."""

    id: int
    is_active: bool

    class Config:
        from_attributes = True
