from fastapi import APIRouter

from app.core.config import settings
from app.schemas.common import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
def healthcheck():
    return HealthResponse(status="ok", service=settings.app_name, version=settings.app_version)
