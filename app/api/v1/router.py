from fastapi import APIRouter

from app.api.v1.routes.ai import router as ai_router
from app.api.v1.routes.analytics import router as analytics_router
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.billing import router as billing_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.leads import router as leads_router
from app.api.v1.routes.tenants import router as tenants_router
from app.api.v1.routes.webhooks import router as webhook_router
from app.api.v1.routes.workflows import router as workflow_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(leads_router, prefix="/leads", tags=["leads"])
api_router.include_router(workflow_router, prefix="/workflows", tags=["workflows"])
api_router.include_router(ai_router, prefix="/ai", tags=["ai"])
api_router.include_router(billing_router, prefix="/billing", tags=["billing"])
api_router.include_router(tenants_router, prefix="/tenants", tags=["tenants"])
api_router.include_router(analytics_router, tags=["analytics"])
api_router.include_router(webhook_router, tags=["webhooks"])
