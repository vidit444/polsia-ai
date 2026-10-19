from functools import lru_cache

from pydantic import AnyHttpUrl, Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(alias="APP_NAME")
    app_env: str = Field(alias="APP_ENV")
    app_host: str = Field(alias="APP_HOST")
    app_port: int = Field(alias="APP_PORT")
    database_url: str = Field(alias="DATABASE_URL")
    jwt_secret: str = Field(alias="JWT_SECRET")
    jwt_algorithm: str = Field(alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_minutes: int = Field(alias="REFRESH_TOKEN_EXPIRE_MINUTES")
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    anthropic_api_key: str = Field(alias="ANTHROPIC_API_KEY")
    ai_default_provider: str = Field(alias="AI_DEFAULT_PROVIDER")
    rate_limit_requests: int = Field(alias="RATE_LIMIT_REQUESTS")
    rate_limit_window_seconds: int = Field(alias="RATE_LIMIT_WINDOW_SECONDS")
    debug_review_interval_seconds: int = Field(alias="DEBUG_REVIEW_INTERVAL_SECONDS")
    webhook_signing_secret: str = Field(alias="WEBHOOK_SIGNING_SECRET")
    upi_qr_url: str = Field(alias="UPI_QR_URL")
    cors_allow_origins: list[str] = Field(alias="CORS_ALLOW_ORIGINS")

    @field_validator(
        "jwt_secret",
        "database_url",
        "openai_api_key",
        "anthropic_api_key",
        "webhook_signing_secret",
        mode="before",
    )
    @classmethod
    def validate_required_secret(cls, value: str) -> str:
        if value is None or not str(value).strip():
            raise ValueError("Required secret/config missing from environment")
        return value

    @field_validator("cors_allow_origins", mode="before")
    @classmethod
    def split_cors(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as exc:
        raise RuntimeError(f"Invalid application configuration: {exc}") from exc
