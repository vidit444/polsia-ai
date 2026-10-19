from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_context, get_db_session
from app.schemas.auth import TokenPayload
from app.schemas.dashboard import DashboardMetricsResponse
from app.services.dashboard_service import get_dashboard_metrics

router = APIRouter()


@router.get("/metrics", response_model=DashboardMetricsResponse)
async def metrics(
    tenant_id: str = Query(...),
    context: TokenPayload = Depends(get_current_context),
    session: AsyncSession = Depends(get_db_session),
) -> DashboardMetricsResponse:
    return await get_dashboard_metrics(session, context, tenant_id)
