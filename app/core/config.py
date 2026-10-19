from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Polsia AI"
    app_env: str = "development"
    app_version: str = "1.0.0"
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
    upi_qr_url: str | None = Field(default=None, alias="UPI_QR_URL")
    debug_review_interval_seconds: int = 60
    ai_default_provider: str = "mock"
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")
    trusted_proxies: list[str] = Field(default_factory=list)

    @property
    def jwt_algorithm(self) -> str:
        return self.algorithm

    @property
    def rate_limit_requests(self) -> int:
        return self.rate_limit_per_minute

    @property
    def rate_limit_window_seconds(self) -> int:
        return 60

    @property
    def billing_webhook_secret(self) -> str:
        return self.webhook_signing_secret

    @field_validator("jwt_secret", "admin_password")
    @classmethod
    def validate_required_secret(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("must be set via environment variable and cannot be empty")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
