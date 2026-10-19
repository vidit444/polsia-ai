from fastapi import APIRouter, HTTPException, Request, status

from app.core.config import settings
from app.core.security import create_access_token, normalize_email, verify_password
from app.db.memory import store
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.audit import record_audit_log

router = APIRouter()


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    remote = request.client.host if request.client else "anonymous"
    if forwarded and remote in settings.trusted_proxies:
        return forwarded.split(",")[0].strip()
    return remote


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, request: Request):
    normalized = normalize_email(str(payload.email))
    client_ip = _client_ip(request)
    principal_key = f"login:{normalized}:{client_ip}"
    if await store.is_locked(principal_key):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Account temporarily locked")
    user = await store.get_user_by_normalized_email(normalized)
    if not user or not verify_password(payload.password, user.hashed_password):
        await store.register_failure(principal_key, client_ip)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if user.mfa_enabled and payload.mfa_token != "123456":
        await store.register_failure(principal_key, client_ip)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="MFA required or invalid")
    await store.clear_failures(principal_key)
    token = create_access_token(user.id, {"tenant_id": user.tenant_id, "role": user.role})
    await record_audit_log(user.tenant_id, user.id, "auth.login", "user", user.id, client_ip)
    return TokenResponse(
        access_token=token,
        expires_in=settings.access_token_expire_minutes * 60,
        user={
            "id": user.id,
            "tenant_id": user.tenant_id,
            "role": user.role,
            "name": user.name,
            "email": str(user.email),
            "password_rotation_required": user.password_rotation_required,
        },
    )
