from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db_session
from app.schemas.ai import AIChatRequest, AIChatResponse
from app.services.ai import AIService

router = APIRouter()


@router.post("/chat", response_model=AIChatResponse)
async def chat(
    payload: AIChatRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> AIChatResponse:
    return await AIService(session).chat(payload, current_user)
