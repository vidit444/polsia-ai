from pydantic import BaseModel, Field


class InvoicePayRequest(BaseModel):
    provider: str = Field(default="upi", min_length=2, max_length=30)
    amount: float = Field(gt=0)
    upi_qr_url: str | None = None


class InvoicePayResponse(BaseModel):
    invoice: dict
    payment: dict
