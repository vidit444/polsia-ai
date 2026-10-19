from functools import lru_cache

from pydantic import AliasChoices, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str
    app_name: str
    api_v1_prefix: str
    database_url: str
    jwt_secret: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    admin_email: str
    admin_password: str
    webhook_signing_secret: str
    openai_api_key: str
    redis_url: str
    default_upi_qr_url: str
    cors_origins: list[str]

    @field_validator("jwt_secret", "admin_password", "webhook_signing_secret", "openai_api_key", mode="before")
    @classmethod
    def validate_secret_not_empty(cls, value: str) -> str:
        if value is None or not str(value).strip():
            raise ValueError("Required secret environment variable is missing or empty")
        return str(value)

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        return [item.strip() for item in str(value).split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
