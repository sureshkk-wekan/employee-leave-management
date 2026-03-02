# Employee Leave Management

A web application for managing employee leave requests, approvals, and balances. Built with **FastAPI** (backend) and **React + Vite + Tailwind** (frontend).

## Features

- **Leave requests** — Employees submit leave (annual, sick, unpaid) with dates and reason
- **Approval workflow** — Managers approve or reject requests
- **Leave balances** — Track entitlement, usage, and remaining days per leave type
- **Policies as data** — Leave types and default entitlements configurable via API (admin)
- **Roles** — Employee, Manager, Admin with clear permissions

## Tech stack

- **Backend:** Python 3.10+, FastAPI, Pydantic v2, JWT auth
- **Frontend:** React 18, Vite, Tailwind CSS, React Router
- **Storage:** In-memory with **JSON file** persistence (`backend/data.json`). No database.

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env        # edit if needed
uvicorn app.main:app --reload --port 8000
```

Seed the JSON store with demo users and leave types:

```bash
python -m scripts.seed_db
```

Demo logins (all roles use the same password):

| Role     | Email                | Password |
|----------|----------------------|----------|
| Admin    | admin@example.com    | admin123 |
| Manager  | manager@example.com  | admin123 |
| Employee | employee@example.com | admin123 |

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). The dev server proxies `/api` to the backend.

### API docs

- Swagger: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- ReDoc: [http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)

## Project layout

```
backend/
  app/
    main.py           # FastAPI app
    config.py         # Settings from env
    store.py          # In-memory + JSON file store (no database)
    auth.py           # JWT and get_current_user
    models.py         # Enums (Role, LeaveRequestStatus)
    schemas/          # Pydantic request/response
    routers/          # auth, users, leave-types, leave-requests, leave-balances
  scripts/
    seed_db.py        # Create demo users and leave types (writes to data.json)
frontend/
  src/
    context/AuthContext.jsx   # Auth state and api() helper
    components/Layout.jsx
    pages/           # Login, Dashboard, LeaveRequest, LeaveHistory, Approvals, Balances
```

## Configuration

- **Backend:** Copy `backend/.env.example` to `backend/.env`. Set `SECRET_KEY` for JWT. Optional: set `DATA_FILE` for the JSON store (default: `backend/data.json`).
- **Frontend:** Copy `frontend/.env.example` to `frontend/.env`. Optional: set `VITE_API_URL` (default `/api`). The dev server proxies `/api` to the backend (port 8000 in `vite.config.js`).

## Documentation

- [spec.md](spec.md) — Application specification (roles, features, API, data model)
- [plan.md](plan.md) — Implementation plan and project structure
- [tasks.md](tasks.md) — Task list and verification checklist

## GitHub

Repository: **employee-leave-management**. To push changes:

```bash
git add .
git commit -m "Your message"
git push origin main
```

Use SSH (`git@github.com:...`) or a Personal Access Token; GitHub no longer accepts account passwords. See [GITHUB_PUSH.md](GITHUB_PUSH.md) for setup details.

## License

MIT
