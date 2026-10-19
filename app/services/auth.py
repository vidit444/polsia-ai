from fastapi import HTTPException, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import create_token, verify_password
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest, TokenPair


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repository = UserRepository(session)
        self.settings = get_settings()

    async def login(self, payload: LoginRequest) -> TokenPair:
        user = await self.user_repository.get_by_email(payload.email)
        is_valid = False
        if user is not None:
            is_valid = await run_in_threadpool(verify_password, payload.password, user.password_hash)
        if user is None or not is_valid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        return TokenPair(
            access_token=create_token(str(user.id), "access", self.settings.access_token_expire_minutes),
            refresh_token=create_token(str(user.id), "refresh", self.settings.refresh_token_expire_minutes),
        )
