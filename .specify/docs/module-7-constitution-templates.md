# Module 7: Constitution.md Templates

**Objective:** Provide copy-paste-ready Constitution templates for different project types so every Spec-Kit feature starts with a clear "Supreme Law" and the AI Builder stays in its lane.

---

## Why Constitution Templates?

- **Determinism over vibes:** The Constitution locks down tech stack, patterns, and non-goals so the AI does not guess.
- **Faster /specify and /plan:** When the Constitution is explicit, the AI asks fewer clarifying questions and produces plans that comply by default.
- **Consistent reviews:** Spec-first PRs plus a shared Constitution make review criteria objective (plan vs. constitution, not opinion).

Use one template as the base for `.specify/memory/constitution.md`, then tailor to your repo.

---

## Template A: Minimal (Greenfield / MVP)

**Best for:** New repos, hackathons, or when you want the lightest guardrails.

```markdown
# [Project Name] Constitution

## Core Principles

1. **Single source of truth:** Requirements live in `.specify/spec.md`; code implements the spec.
2. **Tech stack:** [e.g. React + Vite, Python 3.10+ FastAPI, SQLite].
3. **No scope creep:** Only implement what is in the current spec; no "nice-to-haves" without a spec update.

## Non-Goals (Do Not Touch)

- [e.g. No Redux; use React context.]
- [e.g. No class components; functional components and hooks only.]
- [e.g. No new dependencies without justification in plan.md.]

**Version:** 1.0.0 • **Ratified:** [DATE]
```

---

## Template B: Wekan-Style / Enterprise (Full Sections)

**Best for:** Production apps with security, roles, and audit needs (e.g. Leave Management, HR tools, internal dashboards). Aligns with the curriculum's "Architect vs. Builder" and EARS.

```markdown
# [Project Name] Constitution

This document is the authoritative guide for architecture, security, development standards, and non-goals for this repository.

## Table of Contents

- Project Overview
- Core Tech Stack
- Architectural Principles
- Security & Integrity
- Development Standards
- Non-Goals & Constraints

---

## Project Overview

[2–4 sentences: what the system does, main user roles, and key capabilities.]

## Core Tech Stack

- **Frontend:** [e.g. React (Vite) + Tailwind; hooks and context; no Redux.]
- **Backend:** [e.g. Python 3.10+ FastAPI; RESTful API.]
- **Persistence:** [e.g. SQLite for dev, PostgreSQL for production; schema described in plan/data-model.]
- **Validation:** [e.g. Pydantic v2 for request/response and business rules.]

## Architectural Principles

- **Separation of roles:** [e.g. Unauthenticated, user, admin—enforced at API and UI.]
- **Audit trail:** [e.g. Log material actions with actor and timestamp.]
- **Policy as data:** [e.g. Configurable rules in DB/config, not hardcoded.]
- **Simplicity:** [e.g. Clear feature set and APIs over premature abstraction.]

## Security & Integrity

- **Authentication:** [e.g. All sensitive endpoints require auth; JWT or sessions.]
- **Authorization:** [e.g. Role checks; user can only act on allowed resources.]
- **Secrets:** [e.g. Env or .env only; never commit secrets.]
- **Input hygiene:** [e.g. Validate and sanitize; reject invalid data with clear errors.]

## Development Standards

- **Testing:** [e.g. Unit tests for business logic; integration tests for critical flows.]
- **Formatting:** [e.g. Prettier (frontend), black/ruff (Python).]
- **Documentation:** [e.g. OpenAPI for API; document non-obvious rules in spec/code.]

## Non-Goals & Constraints

- **No [X] in MVP:** [e.g. No LDAP/SAML in v1; simple login only.]
- **No [Y]:** [e.g. No Redux; hooks/context only.]
- **No [Z]:** [e.g. No class components; functional only.]
- **Scope boundary:** [e.g. Do not implement payroll or full HRIS; focus on [scope].]

**Version:** 1.0.0 • **Ratified:** [DATE]
```

---

## Template C: Library-First / CLI (Spec-Kit Style)

**Best for:** CLI tools, libraries, or "library-first" products where every capability is a testable module with a CLI surface.

```markdown
# [PROJECT_NAME] Constitution

## Core Principles

### I. Library-First
Every feature starts as a standalone library. Libraries must be self-contained, independently testable, and documented. No organizational-only libraries; clear purpose required.

### II. CLI Interface
Every library exposes functionality via CLI. Text I/O protocol: stdin/args → stdout; errors → stderr. Support JSON and human-readable formats.

### III. Test-First (Non-Negotiable)
TDD mandatory: tests written → user approved → tests fail → then implement. Red–green–refactor strictly enforced.

### IV. Integration Testing
Required for: new library contract tests, contract changes, inter-service communication, shared schemas.

### V. Observability & Simplicity
Text I/O for debuggability; structured logging. Start simple; YAGNI. No breaking changes without version bump and migration plan.

## Additional Constraints

- Tech stack: [e.g. Python 3.10+, Node 20+, etc.]
- Versioning: [e.g. MAJOR.MINOR.BUILD.]
- No [e.g. global mutable state, undocumented CLI flags].

## Governance

Constitution supersedes ad-hoc practices. Amendments require documentation, approval, and migration plan. All PRs must verify compliance.

**Version:** [X.Y.Z] • **Ratified:** [DATE] • **Last Amended:** [DATE]
```

---

## Template D: API-First / Backend Service

**Best for:** REST/GraphQL services, BFFs, or when the main deliverable is a stable API contract.

```markdown
# [Service Name] Constitution

## Core Principles

1. **API contract first:** Endpoints and request/response shapes are defined in `.specify/` (spec + contracts) before implementation. No backward-incompatible changes without versioning or deprecation.
2. **Stateless:** No server-side session state; auth via tokens or headers.
3. **Idempotency where it matters:** [e.g. Mutations that affect billing or orders must support idempotency keys.]
4. **Observability:** Structured logs; metrics for latency and errors; health and readiness endpoints.

## Tech Stack

- **Runtime:** [e.g. Python 3.10+ / Node 20+.]
- **Framework:** [e.g. FastAPI / Express.]
- **Data:** [e.g. PostgreSQL; migrations only via versioned scripts.]
- **Validation:** [e.g. Pydantic v2 / Zod.]

## Security & Operations

- **Auth:** [e.g. JWT or API keys; no secrets in code.]
- **Rate limiting:** [e.g. Per-client limits on public endpoints.]
- **Input:** Validate and sanitize; return 4xx with clear messages.

## Non-Goals

- [e.g. No server-side rendering.]
- [e.g. No direct DB access from outside this service.]
- [e.g. Scope: only [domain]; no [out-of-scope domain].]

**Version:** 1.0.0 • **Ratified:** [DATE]
```

---

## How to Use These Templates

1. **Choose** the template closest to your project (A–D).
2. **Copy** it into `.specify/memory/constitution.md`.
3. **Replace** placeholders: project name, tech stack, security rules, non-goals.
4. **Run** `/specify` and `/plan`; the AI will use the Constitution for the "Constitution Check" and to stay in lane.
5. **Amend** when the project evolves; document version and ratification date.

---

## Linking to the Rest of the Curriculum

- **Module 2:** The Constitution is the "Supreme Law" inside the Memory Bank (`.specify/`).
- **Module 3:** `/plan` should include a **Constitution Check**; reject plans that violate it.
- **Module 5:** EARS requirements in `spec.md` pair with Constitutional non-goals: the Constitution says *what not to do*, EARS says *when the system shall do what*.
- **Module 6:** AGENTS.md can reference the Constitution (e.g. "Always comply with `.specify/memory/constitution.md`").

---

**Version:** 1.0.0 • **Last updated:** 2026-03-02
