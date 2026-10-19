from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Polsia AI"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    admin_email: str = "admin@example.com"
    admin_password: str = Field(..., alias="ADMIN_PASSWORD")
    database_url: str = Field(..., alias="DATABASE_URL")
    webhook_signing_secret: str = Field(..., alias="WEBHOOK_SIGNING_SECRET")
    rate_limit_per_minute: int = 60
    default_tenant_plan: str = "pro"
    default_tenant_status: str = "active"
    log_level: str = "INFO"
    enable_docs: bool = True
    upi_qr_url: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
