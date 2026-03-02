"""Leave request schemas."""
from datetime import date, datetime
from pydantic import BaseModel, field_validator

from app.models import LeaveRequestStatus


class LeaveRequestBase(BaseModel):
    """Shared fields."""

    leave_type_id: int
    start_date: date
    end_date: date
    reason: str | None = None

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v, info):
        start = info.data.get("start_date")
        if start and v < start:
            raise ValueError("end_date must be >= start_date")
        return v


class LeaveRequestCreate(LeaveRequestBase):
    """Create leave request."""

    pass


class LeaveRequestUpdate(BaseModel):
    """Partial update (e.g. cancel)."""

    status: LeaveRequestStatus | None = None


class LeaveRequestApproveReject(BaseModel):
    """Approve or reject with optional reason."""

    approved: bool
    rejection_reason: str | None = None


class LeaveRequestResponse(LeaveRequestBase):
    """Leave request in API responses."""

    id: int
    user_id: int
    status: LeaveRequestStatus
    approved_by_id: int | None = None
    approved_at: datetime | None = None
    rejection_reason: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
