import hashlib
import hmac

from app.models.domain import Invoice


def process_invoice_payment(invoice: Invoice, provider: str, amount: float, currency: str, upi_qr_url: str | None = None) -> dict:
    if invoice.status == "paid":
        raise ValueError("Invoice already paid")
    if amount != invoice.amount:
        raise ValueError("Amount mismatch")
    if currency != invoice.currency:
        raise ValueError("Currency mismatch")
    return {"status": "captured", "upi_ref": f"UPI-{invoice.id[-8:]}", "upi_qr_url": upi_qr_url, "provider": provider}


def verify_webhook_signature(raw_body: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
