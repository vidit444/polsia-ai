from typing import Any

from pydantic import BaseModel


class WebhookResponse(BaseModel):
    provider: str
    accepted: bool
    idempotency_key: str | None = None
    payload: dict[str, Any]
