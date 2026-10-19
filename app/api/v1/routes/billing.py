from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_context, get_db_session
from app.schemas.auth import TokenPayload
from app.schemas.billing import InvoicePaymentRequest, InvoicePaymentResponse
from app.services.billing_service import capture_invoice_payment

router = APIRouter()


@router.post("/invoice/payments", response_model=InvoicePaymentResponse, status_code=status.HTTP_202_ACCEPTED)
async def invoice_payment(
    payload: InvoicePaymentRequest,
    context: TokenPayload = Depends(get_current_context),
    session: AsyncSession = Depends(get_db_session),
) -> InvoicePaymentResponse:
    return await capture_invoice_payment(session, context, payload)
