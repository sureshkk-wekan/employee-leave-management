"""Enums only (no SQLAlchemy). Used by schemas and auth."""
import enum


class Role(str, enum.Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    ADMIN = "admin"


class LeaveRequestStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
