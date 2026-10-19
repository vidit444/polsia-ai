import hashlib
import hmac
import json

from fastapi import HTTPException, status

from app.core.config import get_settings


class WebhookService:
    def verify_signature(self, body: bytes, signature: str | None) -> None:
        settings = get_settings()
        if not signature:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing signature")
        digest = hmac.new(settings.webhook_signing_secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(digest, signature):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

    def parse_payload(self, body: bytes) -> dict:
        if not body:
            return {}
        return json.loads(body.decode("utf-8"))
