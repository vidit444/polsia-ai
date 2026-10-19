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

    async def dispatch(self, request: Request, call_next):
        client = request.client.host if request.client else "unknown"
        now = time.monotonic()
        queue = self._bucket[client]
        while queue and now - queue[0] > self.window:
            queue.popleft()
        if len(queue) >= self.limit:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
        queue.append(now)
        return await call_next(request)
