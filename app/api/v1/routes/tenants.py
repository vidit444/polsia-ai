from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.schemas.tenant import TenantOnboardRequest, TenantResponse
from app.services.tenant_service import onboard_tenant

router = APIRouter()


@router.post("/onboard", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def onboard(payload: TenantOnboardRequest, session: AsyncSession = Depends(get_db_session)) -> TenantResponse:
    return await onboard_tenant(session, payload)
