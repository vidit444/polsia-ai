from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Polsia AI Platform"
    app_version: str = "1.0.0"
    environment: str = "production"
    jwt_secret: str = "change-this-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    debug_header_name: str = "X-Debug-Interval"
    default_tenant_id: str = "tenant_demo"
    default_admin_email: str = "admin@polsia.ai"
    default_admin_password: str = "Admin@123"
    rate_limit_per_minute: int = 120
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
