"""Auth schemas (login, token)."""
from pydantic import BaseModel


class Token(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Payload we store in JWT."""

    sub: int  # user id
    email: str
    role: str
    exp: int | None = None


class LoginRequest(BaseModel):
    """Login body."""

    email: str
    password: str
