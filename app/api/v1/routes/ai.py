from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_tenant_id
from app.db.session import get_db_session
from app.models.user import User
from app.schemas.ai import AIChatRequest, AIChatResponse
from app.services.ai import AIService

router = APIRouter()


@router.post("/chat", response_model=AIChatResponse)
async def chat(
    payload: AIChatRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
) -> AIChatResponse:
    if payload.tenant_id != tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tenant access denied")
    return await AIService(session).chat(payload, current_user)
