from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Polsia AI Platform"
    app_version: str = "1.0.0"
    environment: str = "production"
    database_url: str = Field(..., alias="DATABASE_URL")
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    debug_header_name: str = "X-Debug-Interval"
    debug_mode: bool = False
    default_tenant_id: str = "tenant_demo"
    default_admin_email: str = Field(..., alias="DEFAULT_ADMIN_EMAIL")
    default_admin_password: str = Field(..., alias="DEFAULT_ADMIN_PASSWORD")
    billing_webhook_secret: str = Field(..., alias="BILLING_WEBHOOK_SECRET")
    trusted_proxies: list[str] = Field(default_factory=lambda: ["127.0.0.1", "::1"])
    rate_limit_per_minute: int = 120
    auth_max_failures: int = 5
    auth_lockout_seconds: int = 900
    bootstrap_admin_on_startup: bool = False
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("jwt_secret", "default_admin_password", "billing_webhook_secret")
    @classmethod
    def validate_required_secrets(cls, value: str) -> str:
        if not value or value.strip() in {
            "change-this-in-production",
            "Admin@123",
            "replace-with-strong-random-secret",
            "replace-with-strong-one-time-password",
            "replace-with-billing-webhook-secret",
        }:
            raise ValueError("A real secret must be provided via environment variables")
        return value.strip()

    @field_validator("trusted_proxies", mode="before")
    @classmethod
    def parse_trusted_proxies(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
