# Implementation Plan: Employee Leave Management System

**Date:** 2026-03-02 | **Spec:** [spec.md](spec.md)  
**Status:** Implemented

---

## Summary

Web application for managing employee leave requests, approvals, and balances. Users authenticate by role (Admin, Manager, Employee). Backend exposes a REST API (FastAPI); frontend is a React SPA (Vite + Tailwind). Persistence is an in-memory store with JSON file (`backend/data.json`); no database. JWT used for authentication; role-based access enforced at API and UI.

---

## Technical Context

| Item | Choice |
|------|--------|
| **Language/Version** | Python 3.10+, JavaScript (React 18) |
| **Backend** | FastAPI, Pydantic v2, python-jose (JWT), passlib (bcrypt) |
| **Frontend** | React 18, Vite, Tailwind CSS, React Router |
| **Storage** | In-memory + JSON file (`backend/data.json`); no database |
| **Testing** | (Optional) pytest (backend), Vitest/React Testing Library (frontend) |
| **Target Platform** | Web (browser); backend runs on Linux/Windows/macOS |
| **Project Type** | Web application (frontend + backend) |
| **Constraints** | No Redux; functional components and hooks only; Tailwind for styling |

---

## Constitution Check

Aligned with [.specify/Constitution.md](.specify/Constitution.md) and [.specify/memory/constitution.md](.specify/memory/constitution.md):

- **Roles:** Employee, Manager, Admin — enforced at API and UI.
- **Auth:** JWT; all leave/approval endpoints require authentication.
- **Persistence:** JSON store (no DB); policy as data (leave types in store).
- **Audit:** Material actions logged (request created, approved, rejected).
- **Stack:** React (Vite) + Tailwind; FastAPI + Pydantic; no class components; no manual styling.

---

## Project Structure

### Documentation

```text
.
├── spec.md              # Application specification (this plan's spec)
├── plan.md              # This file
├── tasks.md             # Task list / implementation checklist
├── README.md            # Quick start and project overview
├── .specify/
│   ├── Constitution.md           # Project constitution (root)
│   └── memory/constitution.md     # Constitution (memory copy)
└── docs/                # (Optional) SDD, diagrams
```

### Source Code

```text
backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, router includes
│   ├── config.py            # Settings (env, secret, data_file)
│   ├── auth.py              # JWT create/verify, get_current_user, require_roles
│   ├── database.py          # (Not used — JSON store only)
│   ├── models.py            # Enums: Role, LeaveRequestStatus
│   ├── store.py             # In-memory + JSON persistence (users, leave_types, etc.)
│   ├── routers/
│   │   ├── auth.py          # POST /login, GET /me
│   │   ├── users.py         # CRUD users (admin)
│   │   ├── leave_types.py   # CRUD leave types (admin), list (all)
│   │   ├── leave_requests.py# Create, list, get, approve/reject
│   │   └── leave_balances.py# List balances
│   └── schemas/             # Pydantic request/response models
├── scripts/
│   └── seed_db.py           # Seed users, leave types, initial balances
├── requirements.txt
├── .env.example
└── data.json                # (Generated) JSON store

frontend/
├── src/
│   ├── main.jsx
│   ├── App.jsx              # Routes, ProtectedRoute
│   ├── index.css            # Tailwind
│   ├── context/
│   │   └── AuthContext.jsx  # Auth state, login, logout, api()
│   ├── components/
│   │   └── Layout.jsx       # Header, nav, outlet
│   └── pages/
│       ├── Login.jsx
│       ├── Dashboard.jsx
│       ├── LeaveRequest.jsx
│       ├── LeaveHistory.jsx
│       ├── Approvals.jsx    # Manager/Admin
│       └── Balances.jsx
├── package.json
├── vite.config.js           # Proxy /api to backend
├── tailwind.config.js
└── .env.example             # VITE_API_URL
```

**Structure decision:** Monorepo with `backend/` and `frontend/`; backend uses a single JSON store (no DB process); frontend uses Vite proxy to backend in development.

---

## Complexity Tracking

No constitution violations. Single backend, single frontend, JSON persistence as per constitution (simplicity over scale).
