from app.models.domain import Invoice


def process_invoice_payment(invoice: Invoice, provider: str, amount: float, upi_qr_url: str | None = None) -> dict:
    if amount < invoice.amount:
        return {"status": "partial", "upi_ref": f"UPI-PARTIAL-{invoice.id[-6:]}"}
    return {"status": "captured", "upi_ref": f"UPI-{invoice.id[-8:]}", "upi_qr_url": upi_qr_url}
