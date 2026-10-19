from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.config import get_settings
from app.db.memory import store


def _resolve_client_ip(request: Request) -> str:
    settings = get_settings()
    remote = request.client.host if request.client else "anonymous"
    forwarded = request.headers.get("x-forwarded-for")
    trusted_proxies = set(getattr(settings, "trusted_proxies", []))
    if forwarded and remote in trusted_proxies:
        return forwarded.split(",")[0].strip()
    return remote


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        settings = get_settings()
        ip = _resolve_client_ip(request)
        tenant = request.headers.get("x-tenant-id", "public")
        user = request.headers.get("authorization", "anonymous")[:32]
        key = f"{tenant}:{user}:{ip}"
        allowed, remaining = await store.consume_rate_limit(key, settings.rate_limit_requests, settings.rate_limit_window_seconds)
        if not allowed:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(settings.rate_limit_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response


def register_middleware(app: FastAPI) -> None:
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RateLimitMiddleware)
