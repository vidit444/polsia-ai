from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, require_roles
from app.db.session import get_db_session
from app.schemas.tenant import TenantOnboardRequest, TenantResponse
from app.services.tenant import TenantService

router = APIRouter()


@router.post("/{tenant_id}/onboard", response_model=TenantResponse, dependencies=[Depends(require_roles("admin", "owner"))])
async def onboard_tenant(
    tenant_id: str,
    payload: TenantOnboardRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> TenantResponse:
    return await TenantService(session).onboard(tenant_id, payload, current_user)
