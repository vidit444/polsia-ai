from fastapi import APIRouter

from app.api.v1.routes.analytics import router as analytics_router
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.webhooks import router as webhook_router
from app.api.v1.routes.workflows import router as workflow_router

api_router = APIRouter()
api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(workflow_router, tags=["workflows"])
api_router.include_router(analytics_router, tags=["analytics"])
api_router.include_router(webhook_router, tags=["webhooks"])
