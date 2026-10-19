import asyncio
import time
from collections import defaultdict, deque

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.config import get_settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        settings = get_settings()
        self.limit = settings.rate_limit_requests
        self.window = settings.rate_limit_window_seconds
        self._bucket: dict[str, deque[float]] = defaultdict(deque)
        self._lock = asyncio.Lock()

    async def dispatch(self, request: Request, call_next):
        client = request.client.host if request.client else "unknown"
        tenant = request.headers.get("X-Tenant-Id", "public")
        principal = request.headers.get("Authorization", "anonymous")[:64]
        key = f"{tenant}:{principal}:{client}"
        now = time.monotonic()

        async with self._lock:
            queue = self._bucket[key]
            while queue and now - queue[0] > self.window:
                queue.popleft()
            if len(queue) >= self.limit:
                return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
            queue.append(now)
            remaining = max(0, self.limit - len(queue))

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
