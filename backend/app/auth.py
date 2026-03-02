"""JWT creation/verification and dependency for current user. Uses store (no DB)."""
from datetime import datetime, timedelta
from types import SimpleNamespace
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings
from app.store import get_user_by_id
from app.models import Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", auto_error=False)


def _get_token_from_request(request: Request) -> str | None:
    """Extract Bearer token from Authorization header (works when proxy strips or OAuth2 scheme misses)."""
    auth = request.headers.get("Authorization") or request.headers.get("authorization")
    if not auth or not auth.startswith("Bearer "):
        return None
    return auth[7:].strip() or None


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: int, email: str, role: str) -> str:
    from datetime import timezone
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    # JWT: exp must be numeric; python-jose requires sub to be a string
    to_encode = {"sub": str(user_id), "email": email, "role": role, "exp": int(expire.timestamp())}
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


async def get_current_user(
    request: Request,
    token: Annotated[str | None, Depends(oauth2_scheme)] = None,
):
    token = token or _get_token_from_request(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id = int(sub)  # JWT may return int/float/str
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except (TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not user.get("is_active", True):
        raise HTTPException(status_code=401, detail="User inactive")
    return SimpleNamespace(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        role=Role(user["role"]) if isinstance(user["role"], str) else user["role"],
        manager_id=user.get("manager_id"),
        is_active=user.get("is_active", True),
    )


def require_roles(*allowed: Role):
    async def _require(current_user: Annotated[SimpleNamespace, Depends(get_current_user)]):
        if current_user.role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return _require


RequireManager = Depends(require_roles(Role.MANAGER, Role.ADMIN))
RequireAdmin = Depends(require_roles(Role.ADMIN))
