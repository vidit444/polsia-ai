from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.db.memory import store
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.audit import record_audit_log

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    users = [user for user in store.list("users") if user.email == payload.email]
    if not users:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user = users[0]
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(user.id, {"tenant_id": user.tenant_id, "role": user.role})
    record_audit_log(user.tenant_id, user.id, "auth.login", "user", user.id)
    return TokenResponse(
        access_token=token,
        expires_in=settings.access_token_expire_minutes * 60,
        user={
            "id": user.id,
            "tenant_id": user.tenant_id,
            "role": user.role,
            "name": user.name,
            "email": str(user.email),
        },
    )
