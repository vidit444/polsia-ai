from fastapi import APIRouter

from app.api.v1.routes import auth, billing, dashboard, health, tenants, workflows

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(billing.router, prefix="/billing", tags=["billing"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
