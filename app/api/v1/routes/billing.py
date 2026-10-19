from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Header, HTTPException, Request

from app.api.deps import get_current_user, get_tenant_id
from app.core.config import settings
from app.db.memory import store
from app.models.domain import Payment, User
from app.schemas.billing import InvoicePayRequest, InvoicePayResponse
from app.services.audit import record_audit_log
from app.services.billing import process_invoice_payment, verify_webhook_signature

router = APIRouter()


@router.post("/invoices/{invoice_id}/pay", response_model=InvoicePayResponse)
async def pay_invoice(
    invoice_id: str,
    payload: InvoicePayRequest,
    request: Request,
    x_signature: str = Header(default=""),
    current_user: User = Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    raw_body = await request.body()
    if not verify_webhook_signature(raw_body, x_signature, settings.billing_webhook_secret):
        raise HTTPException(status_code=401, detail="Invalid signature")
    if not await store.ensure_idempotency(payload.idempotency_key, f"invoice:{invoice_id}", datetime.now(timezone.utc).isoformat()):
        raise HTTPException(status_code=409, detail="Duplicate idempotency key")
    invoice = await store.get("invoices", invoice_id)
    if not invoice or invoice.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if invoice.status == "paid":
        raise HTTPException(status_code=409, detail="Invoice already paid")
    try:
        payment_result = process_invoice_payment(invoice, payload.provider, payload.amount, payload.currency, payload.upi_qr_url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    payment = Payment(
        invoice_id=invoice.id,
        provider=payload.provider,
        amount=payload.amount,
        currency=payload.currency,
        status=payment_result["status"],
        idempotency_key=payload.idempotency_key,
        upi_ref=payment_result["upi_ref"],
    )
    await store.insert("payments", payment)
    invoice = await store.update("invoices", invoice.id, status="paid", payment_ref=payment.upi_ref)
    await record_audit_log(tenant_id, current_user.id, "invoice.pay", "invoice", invoice.id, request.client.host if request.client else None)
    return InvoicePayResponse(invoice=invoice.model_dump(mode="json"), payment=payment.model_dump(mode="json"))
