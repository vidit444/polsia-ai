from fastapi import APIRouter

from app.api.v1.routes import ai, auth, billing, health, leads, workflows

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
api_router.include_router(leads.router, prefix="/v1/leads", tags=["leads"])
api_router.include_router(workflows.router, prefix="/v1/workflows", tags=["workflows"])
api_router.include_router(ai.router, prefix="/v1/ai", tags=["ai"])
api_router.include_router(billing.router, prefix="/v1/billing", tags=["billing"])
