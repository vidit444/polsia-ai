from pydantic import BaseModel, Field


class InvoicePayRequest(BaseModel):
    provider: str = Field(default="upi", min_length=2, max_length=30)
    amount: float = Field(gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    upi_qr_url: str | None = None
    idempotency_key: str = Field(min_length=8, max_length=128)


class InvoicePayResponse(BaseModel):
    invoice: dict
    payment: dict
