from datetime import UTC, datetime
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain import AuditLog, Event, Invoice
from app.schemas.auth import TokenPayload
from app.schemas.billing import InvoicePaymentRequest, InvoicePaymentResponse


async def capture_invoice_payment(
    session: AsyncSession,
    context: TokenPayload,
    payload: InvoicePaymentRequest,
) -> InvoicePaymentResponse:
    result = await session.execute(
        select(Invoice).where(Invoice.id == payload.invoice_id, Invoice.tenant_id == context.tenant_id)
    )
    invoice = result.scalar_one_or_none()
    if invoice is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    if Decimal(str(invoice.amount)) != payload.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment amount mismatch")

    invoice.status = "paid"
    invoice.paid_at = datetime.now(UTC)

    audit = AuditLog(
        tenant_id=context.tenant_id,
        actor_user_id=context.user_id,
        action="invoice.payment.captured",
        entity_type="invoice",
        entity_id=str(invoice.id),
    )
    event = Event(
        tenant_id=context.tenant_id,
        type="invoice.paid",
        payload_json={"invoice_id": str(invoice.id), "payment_reference": payload.payment_reference},
        processed_at=datetime.now(UTC),
        status="processed",
    )
    session.add_all([audit, event])
    await session.commit()

    return InvoicePaymentResponse(
        invoice_id=str(invoice.id),
        status=invoice.status,
        paid_at=invoice.paid_at.isoformat() if invoice.paid_at else None,
        payment_reference=payload.payment_reference,
    )
