"""Leave balance schemas."""
from pydantic import BaseModel, computed_field


class LeaveBalanceResponse(BaseModel):
    """Leave balance in API responses."""

    id: int
    user_id: int
    leave_type_id: int
    year: int
    entitlement_days: int
    carried_over_days: int
    used_days: int

    @computed_field
    @property
    def remaining_days(self) -> int:
        return self.entitlement_days + self.carried_over_days - self.used_days

    class Config:
        from_attributes = True
