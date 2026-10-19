from datetime import UTC, datetime

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/live")
async def live() -> dict[str, str]:
    return {"status": "live", "timestamp": datetime.now(UTC).isoformat()}


@router.get("/ready")
async def ready() -> dict[str, str]:
    return {"status": "ready", "app": settings.app_name}


@router.get("/smoke")
async def smoke() -> dict[str, object]:
    return {
        "status": "ok",
        "checks": [
            "api-router-loaded",
            "settings-loaded",
            "scheduled-health-check-enabled",
        ],
    }
