"""In-memory store with JSON file persistence. No database."""
from __future__ import annotations

import json
import threading
from datetime import date, datetime
from pathlib import Path
from typing import Any

from app.config import settings


def _serialize(obj: Any) -> Any:
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, list):
        return [_serialize(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    return obj


def _next_id(store: dict, key: str) -> int:
    store["_next_id"] = store.get("_next_id", {})
    store["_next_id"][key] = store["_next_id"].get(key, 1)
    n = store["_next_id"][key]
    store["_next_id"][key] = n + 1
    return n


_lock = threading.Lock()


def _data_path() -> Path:
    p = getattr(settings, "data_file", None)
    return Path(p) if p else (Path(__file__).resolve().parent.parent / "data.json")


def _load() -> dict:
    path = _data_path()
    if not path.exists():
        return {
            "users": [],
            "leave_types": [],
            "leave_requests": [],
            "leave_balances": [],
            "audit_logs": [],
            "_next_id": {"users": 1, "leave_types": 1, "leave_requests": 1, "leave_balances": 1, "audit_logs": 1},
        }
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict) -> None:
    path = _data_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(_serialize(data), f, indent=2)


def _get_data() -> dict:
    with _lock:
        return _load()


def _put_data(data: dict) -> None:
    with _lock:
        _save(data)


# --- Users ---

def get_user_by_id(user_id: int) -> dict | None:
    data = _get_data()
    uid = int(user_id)
    for u in data.get("users", []):
        if int(u.get("id", 0)) == uid:
            return u
    return None


def get_user_by_email(email: str) -> dict | None:
    data = _get_data()
    for u in data.get("users", []):
        if u["email"] == email:
            return u
    return None


def list_users() -> list[dict]:
    data = _get_data()
    users = data.get("users", [])
    return sorted(users, key=lambda u: u["email"])


def create_user(
    email: str,
    hashed_password: str,
    full_name: str,
    role: str,
    manager_id: int | None = None,
) -> dict:
    data = _get_data()
    for u in data.get("users", []):
        if u["email"] == email:
            raise ValueError("Email already registered")
    uid = _next_id(data, "users")
    user = {
        "id": uid,
        "email": email,
        "hashed_password": hashed_password,
        "full_name": full_name,
        "role": role,
        "manager_id": manager_id,
        "is_active": True,
    }
    data.setdefault("users", []).append(user)
    _put_data(data)
    return user


def update_user(
    user_id: int,
    full_name: str | None = None,
    role: str | None = None,
    manager_id: int | None = None,
    is_active: bool | None = None,
) -> dict | None:
    data = _get_data()
    for u in data.get("users", []):
        if u["id"] == user_id:
            if full_name is not None:
                u["full_name"] = full_name
            if role is not None:
                u["role"] = role
            if manager_id is not None:
                u["manager_id"] = manager_id
            if is_active is not None:
                u["is_active"] = is_active
            _put_data(data)
            return u
    return None


def update_user_password(user_id: int, hashed_password: str) -> bool:
    """Update a user's password. Returns True if user found."""
    data = _get_data()
    for u in data.get("users", []):
        if u["id"] == user_id:
            u["hashed_password"] = hashed_password
            _put_data(data)
            return True
    return False


# --- Leave types ---

def get_leave_type(leave_type_id: int) -> dict | None:
    data = _get_data()
    for lt in data.get("leave_types", []):
        if lt["id"] == leave_type_id:
            return lt
    return None


def list_leave_types(active_only: bool = True) -> list[dict]:
    data = _get_data()
    types = data.get("leave_types", [])
    if active_only:
        types = [t for t in types if t.get("is_active", True)]
    return sorted(types, key=lambda t: t["name"])


def create_leave_type(
    name: str,
    code: str,
    default_days_per_year: int = 0,
    allow_carry_over: bool = False,
) -> dict:
    data = _get_data()
    for t in data.get("leave_types", []):
        if t["code"] == code:
            raise ValueError("Leave type code already exists")
    lid = _next_id(data, "leave_types")
    lt = {
        "id": lid,
        "name": name,
        "code": code,
        "default_days_per_year": default_days_per_year,
        "allow_carry_over": allow_carry_over,
        "is_active": True,
    }
    data.setdefault("leave_types", []).append(lt)
    _put_data(data)
    return lt


def update_leave_type(
    leave_type_id: int,
    name: str | None = None,
    default_days_per_year: int | None = None,
    allow_carry_over: bool | None = None,
    is_active: bool | None = None,
) -> dict | None:
    data = _get_data()
    for lt in data.get("leave_types", []):
        if lt["id"] == leave_type_id:
            if name is not None:
                lt["name"] = name
            if default_days_per_year is not None:
                lt["default_days_per_year"] = default_days_per_year
            if allow_carry_over is not None:
                lt["allow_carry_over"] = allow_carry_over
            if is_active is not None:
                lt["is_active"] = is_active
            _put_data(data)
            return lt
    return None


# --- Leave requests ---

def _days_between(start: date, end: date) -> int:
    return (end - start).days + 1


def list_leave_requests(
    current_user_id: int,
    current_user_role: str,
    my_only: bool = True,
    status_filter: str | None = None,
) -> list[dict]:
    data = _get_data()
    requests = data.get("leave_requests", [])
    users = {u["id"]: u for u in data.get("users", [])}
    if my_only or current_user_role == "employee":
        requests = [r for r in requests if r["user_id"] == current_user_id]
    elif current_user_role == "manager":
        reportee_ids = {u["id"] for u in users.values() if u.get("manager_id") == current_user_id}
        requests = [r for r in requests if r["user_id"] in reportee_ids]
    if status_filter:
        requests = [r for r in requests if r["status"] == status_filter]
    requests.sort(key=lambda r: r.get("created_at", ""), reverse=True)
    return requests


def get_leave_request(request_id: int) -> dict | None:
    data = _get_data()
    for r in data.get("leave_requests", []):
        if r["id"] == request_id:
            return r
    return None


def create_leave_request(
    user_id: int,
    leave_type_id: int,
    start_date: date,
    end_date: date,
    reason: str | None,
) -> dict:
    data = _get_data()
    rid = _next_id(data, "leave_requests")
    now = datetime.now().isoformat()
    req = {
        "id": rid,
        "user_id": user_id,
        "leave_type_id": leave_type_id,
        "start_date": start_date.isoformat() if isinstance(start_date, date) else start_date,
        "end_date": end_date.isoformat() if isinstance(end_date, date) else end_date,
        "reason": reason,
        "status": "pending",
        "approved_by_id": None,
        "approved_at": None,
        "rejection_reason": None,
        "created_at": now,
        "updated_at": now,
    }
    data.setdefault("leave_requests", []).append(req)
    _put_data(data)
    return req


def update_leave_request_approve(
    request_id: int,
    approved: bool,
    approved_by_id: int,
    rejection_reason: str | None = None,
) -> dict | None:
    data = _get_data()
    now = datetime.now().isoformat()
    for r in data.get("leave_requests", []):
        if r["id"] == request_id:
            r["status"] = "approved" if approved else "rejected"
            r["approved_by_id"] = approved_by_id
            r["approved_at"] = now
            r["rejection_reason"] = None if approved else rejection_reason
            r["updated_at"] = now
            _put_data(data)
            return r
    return None


# --- Leave balances ---

def get_balance(user_id: int, leave_type_id: int, year: int) -> dict | None:
    data = _get_data()
    for b in data.get("leave_balances", []):
        if b["user_id"] == user_id and b["leave_type_id"] == leave_type_id and b["year"] == year:
            return b
    return None


def get_or_create_balance(user_id: int, leave_type_id: int, year: int) -> dict:
    b = get_balance(user_id, leave_type_id, year)
    if b:
        return b
    lt = get_leave_type(leave_type_id)
    default_days = lt["default_days_per_year"] if lt else 0
    data = _get_data()
    bid = _next_id(data, "leave_balances")
    balance = {
        "id": bid,
        "user_id": user_id,
        "leave_type_id": leave_type_id,
        "year": year,
        "entitlement_days": default_days,
        "carried_over_days": 0,
        "used_days": 0,
    }
    data.setdefault("leave_balances", []).append(balance)
    _put_data(data)
    return balance


def add_used_days(user_id: int, leave_type_id: int, year: int, days: int) -> None:
    data = _get_data()
    for b in data.get("leave_balances", []):
        if b["user_id"] == user_id and b["leave_type_id"] == leave_type_id and b["year"] == year:
            b["used_days"] = b.get("used_days", 0) + days
            _put_data(data)
            return
    # create and add
    bal = get_or_create_balance(user_id, leave_type_id, year)
    bal["used_days"] = bal.get("used_days", 0) + days
    data = _get_data()
    for b in data.get("leave_balances", []):
        if b["id"] == bal["id"]:
            b["used_days"] = bal["used_days"]
            _put_data(data)
            return


def list_leave_balances(user_id: int, year: int | None = None) -> list[dict]:
    data = _get_data()
    balances = [b for b in data.get("leave_balances", []) if b["user_id"] == user_id]
    if year is not None:
        balances = [b for b in balances if b["year"] == year]
    balances.sort(key=lambda b: (-b["year"], b["leave_type_id"]))
    return balances


# --- Audit ---

def log_action(
    action: str,
    actor_id: int | None = None,
    target_type: str | None = None,
    target_id: int | None = None,
    details: str | None = None,
) -> None:
    data = _get_data()
    aid = _next_id(data, "audit_logs")
    entry = {
        "id": aid,
        "action": action,
        "actor_id": actor_id,
        "target_type": target_type,
        "target_id": target_id,
        "details": details,
        "created_at": datetime.now().isoformat(),
    }
    data.setdefault("audit_logs", []).append(entry)
    _put_data(data)
