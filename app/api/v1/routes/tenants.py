from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session, require_roles
from app.models.domain import User
from app.schemas.tenant import TenantOnboardRequest, TenantResponse
from app.services.tenant_service import onboard_tenant

router = APIRouter()


@router.post("/onboard", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def onboard(
    payload: TenantOnboardRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(require_roles("admin")),
) -> TenantResponse:
    return await onboard_tenant(session, payload)
