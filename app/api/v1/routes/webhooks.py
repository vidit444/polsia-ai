from fastapi import APIRouter, Depends, Header, Request, status

from app.api.deps import get_idempotency_key
from app.schemas.webhook import WebhookResponse
from app.services.webhook import WebhookService

router = APIRouter(prefix="/webhooks")
service = WebhookService()


@router.post("/{provider}", response_model=WebhookResponse, status_code=status.HTTP_202_ACCEPTED)
async def ingest_webhook(
    provider: str,
    request: Request,
    idempotency_key: str | None = Depends(get_idempotency_key),
    x_signature: str | None = Header(default=None, alias="X-Signature"),
) -> WebhookResponse:
    body = await request.body()
    service.verify_signature(body, x_signature)
    payload = service.parse_payload(body)
    return WebhookResponse(provider=provider, accepted=True, idempotency_key=idempotency_key, payload=payload)
