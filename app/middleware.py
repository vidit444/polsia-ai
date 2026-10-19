from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.config import settings
from app.db.memory import store


def _resolve_client_ip(request: Request) -> str:
    remote = request.client.host if request.client else "anonymous"
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded and remote in settings.trusted_proxies:
        return forwarded.split(",")[0].strip()
    return remote


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = _resolve_client_ip(request)
        tenant = request.headers.get("x-tenant-id", "public")
        user = request.headers.get("authorization", "anonymous")[:32]
        key = f"{tenant}:{user}:{ip}"
        allowed, remaining = await store.consume_rate_limit(key, settings.rate_limit_per_minute, 60)
        if not allowed:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(settings.rate_limit_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        if settings.debug_mode:
            response.headers[settings.debug_header_name] = "weekly-debug-sprint"
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
