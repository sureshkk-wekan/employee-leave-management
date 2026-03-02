# Tasks: Employee Leave Management System

**Spec:** [spec.md](spec.md) | **Plan:** [plan.md](plan.md)  
**Status:** Implemented (checklist for verification and future work)

---

## Format

- `[P]` = Can run in parallel (different files, no dependencies)
- `[Story]` = User-story label where applicable (Auth, Leave, Balances, Users, Admin)
- Paths: `backend/`, `frontend/` per [plan.md](plan.md)

---

## Phase 1: Setup & Foundation

- [x] T001 Create project structure: `backend/`, `frontend/`, root config files
- [x] T002 Backend: Python venv, `requirements.txt`, FastAPI app in `backend/app/main.py`
- [x] T003 Frontend: Vite + React + Tailwind, `frontend/package.json`, `vite.config.js`
- [x] T004 [P] Backend config: `backend/app/config.py` (env, secret key, data file path)
- [x] T005 [P] Frontend env: `frontend/.env.example` with `VITE_API_URL`
- [x] T006 Store: `backend/app/store.py` — load/save JSON, users, leave_types, leave_requests, leave_balances, audit_logs
- [x] T007 Auth: `backend/app/auth.py` — JWT create/verify, `get_current_user`, `require_roles`
- [x] T008 Seed: `backend/scripts/seed_db.py` — demo users (admin, manager, employee), leave types, initial balances

---

## Phase 2: Authentication (Auth)

**Goal:** Users can log in with email/password and receive a JWT; frontend stores token and sends it on API calls.

- [x] T009 [Auth] POST `/api/auth/login` — validate credentials, return JWT (`backend/app/routers/auth.py`)
- [x] T010 [Auth] GET `/api/auth/me` — return current user from JWT (`backend/app/routers/auth.py`)
- [x] T011 [Auth] Frontend: `AuthContext` — login, logout, `api()` helper, token in localStorage (`frontend/src/context/AuthContext.jsx`)
- [x] T012 [Auth] Frontend: Login page — form, redirect after login (`frontend/src/pages/Login.jsx`)
- [x] T013 [Auth] Frontend: Protected routes and role-based redirect (`frontend/src/App.jsx`)

---

## Phase 3: Leave Types (Admin)

**Goal:** Admin can create/update leave types; all authenticated users can list active leave types.

- [x] T014 [P] GET `/api/leave-types` — list (optional active_only) (`backend/app/routers/leave_types.py`)
- [x] T015 POST `/api/leave-types` — create (admin only)
- [x] T016 GET `/api/leave-types/{id}` — get one
- [x] T017 PATCH `/api/leave-types/{id}` — update (admin only)
- [x] T018 Frontend: Leave type dropdown in Request Leave page (uses `/api/leave-types`)

---

## Phase 4: Leave Requests (Leave)

**Goal:** Employees submit leave requests; managers/admins approve or reject; balance validated on submit and updated on approve.

- [x] T019 [Leave] POST `/api/leave-requests` — create (validate balance, dates) (`backend/app/routers/leave_requests.py`)
- [x] T020 [Leave] GET `/api/leave-requests` — list (own or team for manager; query: status, my_only)
- [x] T021 [Leave] GET `/api/leave-requests/{id}` — get one (owner or manager/admin)
- [x] T022 [Leave] POST `/api/leave-requests/{id}/approve` — approve/reject (manager/admin); update balance on approve
- [x] T023 [Leave] Store: `get_or_create_balance`, `add_used_days`, audit log on approve/reject (`backend/app/store.py`)
- [x] T024 [Leave] Frontend: Request Leave page — form, submit to POST `/api/leave-requests` (`frontend/src/pages/LeaveRequest.jsx`)
- [x] T025 [Leave] Frontend: My Requests page — list, status, leave type name (`frontend/src/pages/LeaveHistory.jsx`)
- [x] T026 [Leave] Frontend: Approvals page — pending list, Approve/Reject (manager/admin) (`frontend/src/pages/Approvals.jsx`)

---

## Phase 5: Leave Balances (Balances)

**Goal:** Users view leave balances (entitlement, used, remaining) per leave type and year.

- [x] T027 [Balances] GET `/api/leave-balances` — list (own; admin can pass user_id, year) (`backend/app/routers/leave_balances.py`)
- [x] T028 [Balances] Frontend: My Balances page — list with remaining_days, leave type name (`frontend/src/pages/Balances.jsx`)
- [x] T029 [Balances] Seed: create initial leave_balances for all users and leave types for current year (`backend/scripts/seed_db.py`)

---

## Phase 6: User Management (Users / Admin)

**Goal:** Admin can list, create, get, and update users (roles, manager_id, is_active).

- [x] T030 [Users] GET `/api/users` — list (admin only) (`backend/app/routers/users.py`)
- [x] T031 [Users] POST `/api/users` — create (admin only; hash password)
- [x] T032 [Users] GET `/api/users/{id}` — get one (self or admin)
- [x] T033 [Users] PATCH `/api/users/{id}` — update (admin only)
- [x] T034 [Users] Store: `update_user`, `update_user_password` for demo password sync (`backend/app/store.py`)

---

## Phase 7: UI & Integration

- [x] T035 Layout: Header, nav (Dashboard, Request Leave, My Requests, My Balances, Approvals for manager/admin), user name, Logout (`frontend/src/components/Layout.jsx`)
- [x] T036 Dashboard: Welcome and links to main actions (`frontend/src/pages/Dashboard.jsx`)
- [x] T037 Vite proxy: `/api` → backend (e.g. `http://127.0.0.1:8000`) (`frontend/vite.config.js`)
- [x] T038 CORS: Backend allows frontend origin (`backend/app/main.py`)
- [x] T039 Demo credentials: All roles use password `admin123`; seed updates existing demo users to admin123

---

## Phase 8: Documentation & Repo

- [x] T040 README: Quick start, tech stack, project layout, demo logins, config (`README.md`)
- [x] T041 spec.md: Application specification aligned with implementation
- [x] T042 plan.md: Implementation plan (technical context, structure, constitution check)
- [x] T043 tasks.md: This task list
- [x] T044 .specify/Constitution.md and .specify/memory/constitution.md updated (JSON store, JWT)

---

## Optional / Future

- [ ] T045 Add unit tests: leave balance logic, date validation (`backend/tests/`)
- [ ] T046 Add API integration tests: login → request → approve → balance (`backend/tests/`)
- [ ] T047 Add frontend tests: Login, ProtectedRoute, key flows (`frontend/src/`)
- [ ] T048 Calendar or list view of approved leave for planning
- [ ] T049 Optional: Switch persistence to SQLite/PostgreSQL (schema in plan/spec)

---

## Dependencies & Order

- **Phase 1** must be done first (store, auth, seed).
- **Phase 2** (Auth) blocks all authenticated features.
- **Phases 3–6** can be understood in order Leave Types → Leave Requests → Balances → Users; implementation may overlap.
- **Phase 7** ties frontend to backend (proxy, CORS, layout).
- **Phase 8** documents the current state.

---

## Verification Checklist

1. Run `backend/scripts/seed_db.py` — creates users and leave types.
2. Start backend: `uvicorn app.main:app --reload --port 8000`.
3. Start frontend: `npm run dev` in `frontend/`.
4. Log in as admin@example.com / admin123, manager@example.com / admin123, employee@example.com / admin123.
5. As employee: submit a leave request; as manager/admin: open Approvals and approve; as employee: check My Balances and My Requests.
