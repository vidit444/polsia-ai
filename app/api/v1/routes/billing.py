from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.deps import get_current_user, get_tenant_id
from app.db.memory import store
from app.models.domain import Payment, User
from app.schemas.billing import InvoicePayRequest, InvoicePayResponse
from app.services.audit import record_audit_log
from app.services.billing import process_invoice_payment

router = APIRouter()


@router.post("/invoices/{invoice_id}/pay", response_model=InvoicePayResponse)
def pay_invoice(invoice_id: str, payload: InvoicePayRequest, request: Request, current_user: User = Depends(get_current_user), tenant_id: str = Depends(get_tenant_id)):
    invoice = store.get("invoices", invoice_id)
    if not invoice or invoice.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Invoice not found")
    payment_result = process_invoice_payment(invoice, payload.provider, payload.amount, payload.upi_qr_url)
    payment = Payment(invoice_id=invoice.id, provider=payload.provider, amount=payload.amount, status=payment_result["status"], upi_ref=payment_result["upi_ref"])
    store.insert("payments", payment)
    invoice.status = "paid"
    invoice.payment_ref = payment.upi_ref
    record_audit_log(tenant_id, current_user.id, "invoice.pay", "invoice", invoice.id, request.client.host if request.client else None)
    return InvoicePayResponse(invoice=invoice.model_dump(mode="json"), payment=payment.model_dump(mode="json"))
