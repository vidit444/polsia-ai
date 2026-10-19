from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_tenant_id
from app.db.session import get_db_session
from app.schemas.analytics import DashboardAnalyticsResponse
from app.services.analytics import AnalyticsService

router = APIRouter()


@router.get("/dashboard", response_model=DashboardAnalyticsResponse)
async def dashboard(
    tenant_id: str = Depends(get_tenant_id),
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> DashboardAnalyticsResponse:
    return await AnalyticsService(session).dashboard(tenant_id, current_user)
