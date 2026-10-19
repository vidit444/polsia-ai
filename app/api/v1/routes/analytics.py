from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.analytics import KPIResponse
from app.services.analytics import AnalyticsService

router = APIRouter(prefix="/tenants/{tenant_id}/analytics")
service = AnalyticsService()


@router.get("/kpis", response_model=KPIResponse)
async def get_kpis(tenant_id: str, db=Depends(get_db), user: dict = Depends(get_current_user)) -> KPIResponse:
    if user.get("tenant_id") != tenant_id:
        raise HTTPException(status_code=403, detail="Tenant access denied")
    result = service.get_kpis(db, tenant_id)
    return KPIResponse(**result)
