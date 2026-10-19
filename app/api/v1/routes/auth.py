from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.auth import LoginRequest, TokenPair
from app.services.auth import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_db_session)) -> TokenPair:
    return await AuthService(session).login(payload)
