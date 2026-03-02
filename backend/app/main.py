"""Employee Leave Management API — FastAPI application. Uses in-memory + JSON store (no database)."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, leave_requests, leave_types, leave_balances, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """No DB to init; store loads from JSON on first use."""
    yield


app = FastAPI(
    title=settings.app_name,
    description="RESTful API for leave requests, approvals, and balances. Data stored in JSON file.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(leave_requests.router, prefix="/api")
app.include_router(leave_types.router, prefix="/api")
app.include_router(leave_balances.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Employee Leave Management API (JSON store)", "docs": "/api/docs"}
