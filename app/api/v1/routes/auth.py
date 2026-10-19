from fastapi import APIRouter

from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth")
service = AuthService()


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest) -> TokenResponse:
    token = service.login(payload.email, payload.password, payload.tenant_id)
    return TokenResponse(access_token=token)
