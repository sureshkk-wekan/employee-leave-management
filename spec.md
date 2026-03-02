# Application Specification: Employee Leave Management System

**Version:** 1.0  
**Last updated:** 2026-03-02  
**Status:** Implemented

---

## 1. Overview

The **Employee Leave Management System** is a web application for organizations to manage employee leave requests, approvals, and leave balances. Users log in by role (Admin, Manager, Employee); employees request leave, managers approve or reject, and the system tracks balances per leave type.

---

## 2. Scope

- **In scope:** Leave requests (create, list, approve/reject), leave types (CRUD by admin), leave balances (view, auto-update on approval), user management (admin), authentication (JWT), role-based access.
- **Out of scope:** Payroll, attendance clock-in/out, full HRIS, LDAP/SAML/SSO in MVP, calendar view (future).

---

## 3. Roles & Permissions

| Role      | Description           | Permissions |
|-----------|-----------------------|-------------|
| **Admin** | System administrator  | All: manage users, leave types; approve any request; view any balance; CRUD users. |
| **Manager** | Team manager        | Approve/reject leave for reportees; view own and reportees’ requests; view own balance. |
| **Employee** | Staff member       | Submit leave requests; view own requests and own balances only. |

- Authentication: email + password; JWT issued on login.
- Authorization: enforced at API and UI (e.g. Approvals page only for Manager/Admin).

---

## 4. Core Features

### 4.1 Authentication

- **Login:** POST `/api/auth/login` with `email`, `password`; returns `access_token` (JWT).
- **Current user:** GET `/api/auth/me` with `Authorization: Bearer <token>`; returns user profile (id, email, full_name, role, manager_id, is_active).
- Token stored in frontend (e.g. localStorage); sent on all API requests.

### 4.2 Leave Types

- **List:** GET `/api/leave-types` (authenticated); optional `active_only`.
- **Create:** POST `/api/leave-types` (admin only); body: name, code, default_days_per_year, allow_carry_over.
- **Get one:** GET `/api/leave-types/{id}`.
- **Update:** PATCH `/api/leave-types/{id}` (admin only).

Attributes: id, name, code, default_days_per_year, allow_carry_over, is_active.

### 4.3 Leave Requests

- **Create:** POST `/api/leave-requests`; body: leave_type_id, start_date, end_date, reason (optional). Validates balance and date range.
- **List:** GET `/api/leave-requests`; query: `status` (pending/approved/rejected/cancelled), `my_only` (true for own, false for managers: team).
- **Get one:** GET `/api/leave-requests/{id}` (owner or manager/admin).
- **Approve/Reject:** POST `/api/leave-requests/{id}/approve`; body: approved (bool), rejection_reason (optional). Manager/admin only; on approve, used_days are added to the relevant leave balance.

Status values: pending, approved, rejected, cancelled.

### 4.4 Leave Balances

- **List:** GET `/api/leave-balances`; optional query: user_id (admin only), year.
- Response includes: user_id, leave_type_id, year, entitlement_days, carried_over_days, used_days, remaining_days (computed).

Balances are created on first use (e.g. when submitting a request or by seed); entitlement comes from leave type default.

### 4.5 Users

- **List:** GET `/api/users` (admin only).
- **Create:** POST `/api/users` (admin only); body: email, password, full_name, role, manager_id (optional).
- **Get one:** GET `/api/users/{id}` (self or admin).
- **Update:** PATCH `/api/users/{id}` (admin only); body: full_name, role, manager_id, is_active.

---

## 5. Data Model (Store)

Persistence: in-memory store with JSON file (`backend/data.json`). No database.

- **users:** id, email, hashed_password, full_name, role (employee|manager|admin), manager_id (nullable), is_active.
- **leave_types:** id, name, code, default_days_per_year, allow_carry_over, is_active.
- **leave_requests:** id, user_id, leave_type_id, start_date, end_date, reason, status, approved_by_id, approved_at, rejection_reason, created_at, updated_at.
- **leave_balances:** id, user_id, leave_type_id, year, entitlement_days, carried_over_days, used_days.
- **audit_logs:** id, action, actor_id, target_type, target_id, details, created_at.

---

## 6. API Summary

| Method | Endpoint | Auth | Role |
|--------|----------|------|------|
| POST   | /api/auth/login | No | - |
| GET    | /api/auth/me | Yes | Any |
| GET    | /api/leave-types | Yes | Any |
| POST   | /api/leave-types | Yes | Admin |
| GET    | /api/leave-types/{id} | Yes | Any |
| PATCH  | /api/leave-types/{id} | Yes | Admin |
| POST   | /api/leave-requests | Yes | Any |
| GET    | /api/leave-requests | Yes | Any |
| GET    | /api/leave-requests/{id} | Yes | Owner / Manager / Admin |
| POST   | /api/leave-requests/{id}/approve | Yes | Manager / Admin |
| GET    | /api/leave-balances | Yes | Any (admin can pass user_id) |
| GET    | /api/users | Yes | Admin |
| POST   | /api/users | Yes | Admin |
| GET    | /api/users/{id} | Yes | Self / Admin |
| PATCH  | /api/users/{id} | Yes | Admin |

---

## 7. Frontend (UI) Structure

- **Login:** Single page; email, password; redirect to dashboard on success.
- **Layout:** Header with nav (Dashboard, Request Leave, My Requests, My Balances, Approvals for manager/admin), user name, Logout.
- **Dashboard:** Welcome and shortcuts to main actions.
- **Request Leave:** Form: leave type, start date, end date, reason; submit creates request.
- **My Requests:** List of current user’s leave requests with status (pending/approved/rejected).
- **My Balances:** List of leave balances (by type/year) with remaining days.
- **Approvals:** List of pending requests (for reportees or all for admin); Approve / Reject actions.

All demo roles use the same password: **admin123**. Demo users: admin@example.com, manager@example.com, employee@example.com.

---

## 8. Tech Stack

- **Frontend:** React 18, Vite, Tailwind CSS, React Router; hooks and context (no Redux); functional components only.
- **Backend:** Python 3.10+, FastAPI, Pydantic v2; JWT (python-jose), bcrypt for passwords.
- **Persistence:** JSON file store (`backend/data.json`); no database.
- **Config:** Backend: `.env` (e.g. SECRET_KEY, optional DATA_FILE). Frontend: `.env` with VITE_API_URL (default `/api` for proxy).

---

## 9. Business Rules (Summary)

- End date must be ≥ start date for leave requests.
- Leave request is only allowed if remaining balance (entitlement + carried_over − used) ≥ requested days for that leave type and year.
- Only pending requests can be approved or rejected.
- Managers may only approve requests for their reportees (users whose manager_id is the current user).
- On approval, used_days for the relevant leave balance (user, leave type, year) are increased by the number of calendar days in the request.
- Material actions (e.g. request created, approved, rejected) are recorded in audit_logs with actor and timestamp.

---

This specification reflects the implemented Employee Leave Management application as of the date above.
