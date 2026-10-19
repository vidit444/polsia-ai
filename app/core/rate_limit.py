from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import get_settings


def _default_limit() -> str:
    settings = get_settings()
    return f"{settings.rate_limit_per_minute}/minute"


limiter = Limiter(key_func=get_remote_address, default_limits=[_default_limit()])
