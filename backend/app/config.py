"""Application configuration from environment."""
from pydantic_settings import BaseSettings


# Single fixed secret when SECRET_KEY is not set — tokens then always work across restarts
_DEV_SECRET = "leave-mgmt-dev-secret-key-set-SECRET_KEY-in-production"


def _get_or_create_secret_key(env_value: str | None) -> str:
    """Use env SECRET_KEY if set; otherwise always use fixed dev secret (no .jwt_secret)."""
    if env_value and env_value.strip() and env_value != "change-me-in-production-use-env":
        return env_value
    return _DEV_SECRET


class Settings(BaseSettings):
    """Settings loaded from env or .env file."""

    app_name: str = "Employee Leave Management API"
    debug: bool = False
    data_file: str | None = None  # path to data.json; default backend/data.json
    secret_key: str | None = None  # set via env; else random key in .jwt_secret
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


_settings = Settings()
# Resolve secret_key: env → .jwt_secret file → generate and persist random
settings = type("Settings", (), {
    "app_name": _settings.app_name,
    "debug": _settings.debug,
    "data_file": _settings.data_file,
    "secret_key": _get_or_create_secret_key(getattr(_settings, "secret_key", None)),
    "algorithm": _settings.algorithm,
    "access_token_expire_minutes": _settings.access_token_expire_minutes,
})()
