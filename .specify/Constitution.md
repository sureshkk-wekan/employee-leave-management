<!-- Project Constitution — Employee Leave Management System -->

This document is the authoritative guide for architecture, security, development standards, and non-goals for the "Employee Leave Management System" repository. It governs how leave requests, approvals, balances, and policies are implemented and maintained.

## Table of contents

- Project Overview
- Core Tech Stack
- Architectural Principles
- Security & Integrity
- Development Standards
- Non-Goals & Constraints

---

## Project Overview

The **Employee Leave Management System** is a web application that enables organizations to manage employee leave requests, approvals, and balances. It features:

- **Leave Requests** — Employees submit leave (annual, sick, unpaid, etc.) with dates and reason; requests follow a configurable approval workflow.
- **Approval Workflow** — Managers (or designated approvers) review, approve, or reject requests; optional multi-level approval and delegation.
- **Leave Balances** — Track accruals, usage, and remaining balance per leave type per employee; support for annual entitlement and carry-over rules.
- **Policies & Calendar** — Define leave types, entitlements, and rules; provide a calendar or list view of approved leave for planning and conflict checks.

## Core Tech Stack

- **Frontend:** React (Vite) with Tailwind CSS; use hooks and context for state; keep components focused and reusable.
- **Backend:** Python 3.10+ with FastAPI; RESTful API for leave, users, and approvals.
- **Persistence:** In-memory store with JSON file persistence (`backend/data.json`); schema for users, leave types, requests, approvals, balance snapshots, and audit log. No database required for default setup.
- **Validation:** Pydantic v2 for request/response models and business-rule validation (e.g. date ranges, balance checks).

## Architectural Principles

- **Clear Separation of Roles:** Distinguish unauthenticated, employee, manager, and admin capabilities; enforce at API and UI level.
- **Audit Trail:** Log material actions (request created, approved, rejected, balance adjusted) with actor and timestamp for compliance and debugging.
- **Policy as Data:** Leave types, entitlements, and approval rules are stored as data (e.g. in store/config) rather than hardcoded, to allow changes without code deploys.
- **Simplicity over Scale:** Prefer a small, well-defined feature set and clear APIs over premature abstraction or enterprise plugins.

## Security & Integrity

- **Authentication:** All leave and approval endpoints require authenticated users; JWT in use; never expose approval actions to unauthenticated or wrong-role users.
- **Authorization:** Enforce role checks (e.g. only managers can approve; only admins can change policies or user roles); validate that the acting user is allowed to act on the target resource (e.g. approver for that employee or department).
- **Secrets & Config:** Store secrets (session secret, API keys) in environment or `.env`; never commit secrets to the repository.
- **Input Hygiene:** Validate and sanitize all inputs (dates, leave type IDs, user IDs); reject invalid or out-of-range data with clear error messages.

## Development Standards

- **Testing:** Unit tests for leave balance logic, date-range validation, and approval rules; integration tests for critical API flows (submit → approve → balance update).
- **Formatting:** Use Prettier for frontend and `black`/`ruff` for Python (or project-standard formatters); keep style consistent.
- **Documentation:** Document API endpoints (e.g. OpenAPI/Swagger) and document non-obvious business rules (e.g. how carry-over or overlapping requests are handled) in code or specs.

## Non-Goals & Constraints

- **No Legacy SSO in MVP:** Do not mandate LDAP/SAML/OAuth in the first version unless specified; simple login (e.g. email/password or one IdP) is acceptable for initial scope.
- **No Redux:** Use React hooks and context (or a minimal state library if agreed) instead of Redux.
- **No Class Components:** Use React functional components and hooks only.
- **No Manual Styling:** Use Tailwind (or the chosen design system) for layout and styling; avoid inline styles or unshared CSS for core UI.
- **Scope Boundary:** Do not implement payroll, attendance clock-in/out, or full HRIS; focus on leave requests, approvals, balances, and basic policy configuration.

---

**Version:** 1.1.0  •  **Ratified:** 2026-02-26  •  **Updated:** 2026-03-02 (Persistence: JSON store; JWT)
