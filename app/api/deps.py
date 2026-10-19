from fastapi import Depends, Header, HTTPException, Request, status
from jose import JWTError, jwt

from app.core.config import get_settings
from app.db.memory import store
from app.models.domain import User


async def get_current_user(authorization: str | None = Header(default=None)) -> User:
    settings = get_settings()
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    user_id = payload.get("sub")
    user = await store.get("users", user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def get_tenant_id(
    request: Request,
    current_user: User = Depends(get_current_user),
) -> str:
    tenant_id = request.headers.get("X-Tenant-Id") or current_user.tenant_id
    if tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tenant isolation violation")
    return tenant_id
