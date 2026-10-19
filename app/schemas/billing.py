from decimal import Decimal

from pydantic import BaseModel, Field


class InvoicePaymentRequest(BaseModel):
    invoice_id: str
    amount: Decimal = Field(gt=0)
    currency: str
    payment_reference: str


class InvoicePaymentResponse(BaseModel):
    invoice_id: str
    status: str
    paid_at: str | None
    payment_reference: str
