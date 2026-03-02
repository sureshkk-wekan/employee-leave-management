"""Seed in-memory + JSON store with initial users and leave types. Run from backend: python -m scripts.seed_db."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.auth import hash_password
from app.store import (
    get_user_by_email,
    create_user,
    update_user_password,
    create_leave_type,
    get_or_create_balance,
    list_users,
    list_leave_types,
)
from app.models import Role


def seed():
    # Users
    if get_user_by_email("admin@example.com") is None:
        create_user(
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            full_name="Admin User",
            role=Role.ADMIN.value,
        )
        print("Created admin@example.com / admin123")

    if get_user_by_email("manager@example.com") is None:
        admin = get_user_by_email("admin@example.com")
        create_user(
            email="manager@example.com",
            hashed_password=hash_password("admin123"),
            full_name="Manager User",
            role=Role.MANAGER.value,
            manager_id=admin["id"],
        )
        print("Created manager@example.com / admin123")

    if get_user_by_email("employee@example.com") is None:
        mgr = get_user_by_email("manager@example.com")
        create_user(
            email="employee@example.com",
            hashed_password=hash_password("admin123"),
            full_name="Employee User",
            role=Role.EMPLOYEE.value,
            manager_id=mgr["id"],
        )
        print("Created employee@example.com / admin123")

    # Ensure all demo users use same password (admin123) for easy login
    demo_password = hash_password("admin123")
    updated = 0
    for u in list_users():
        if u["email"] in ("admin@example.com", "manager@example.com", "employee@example.com"):
            if update_user_password(u["id"], demo_password):
                updated += 1
    if updated:
        print("Demo logins (all use password admin123): admin@example.com, manager@example.com, employee@example.com")

    # Leave types
    for code, name, days in [("ANNUAL", "Annual Leave", 22), ("SICK", "Sick Leave", 10), ("UNPAID", "Unpaid Leave", 0)]:
        existing = next((t for t in list_leave_types(active_only=False) if t.get("code") == code), None)
        if not existing:
            create_leave_type(
                name=name,
                code=code,
                default_days_per_year=days,
                allow_carry_over=(code == "ANNUAL"),
            )
            print(f"Created leave type: {code}")

    # Initial leave balances for current year
    from datetime import datetime, timezone
    year = datetime.now(timezone.utc).year
    types = list_leave_types(active_only=False)
    for u in list_users():
        for lt in types:
            get_or_create_balance(u["id"], lt["id"], year)
    print("Seed done.")


if __name__ == "__main__":
    seed()
