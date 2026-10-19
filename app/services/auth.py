from fastapi import HTTPException, status

from app.core.config import get_settings
from app.core.security import create_access_token, verify_password


class AuthService:
    def login(self, email: str, password: str, tenant_id: str) -> str:
        settings = get_settings()
        if email != settings.admin_email or not verify_password(password, settings.admin_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return create_access_token(subject=email, tenant_id=tenant_id, role="admin", user_id=email)
