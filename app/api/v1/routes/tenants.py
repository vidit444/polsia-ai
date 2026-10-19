from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, require_roles
from app.db.session import get_db_session
from app.models.user import User
from app.schemas.tenant import TenantOnboardRequest, TenantResponse
from app.services.tenant import TenantService

router = APIRouter()


@router.post("/{tenant_id}/onboard", response_model=TenantResponse, dependencies=[Depends(require_roles("admin", "owner"))])
async def onboard_tenant(
    tenant_id: str,
    payload: TenantOnboardRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> TenantResponse:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only platform admins can onboard arbitrary tenants",
        )
    return await TenantService(session).onboard(tenant_id, payload, current_user)
