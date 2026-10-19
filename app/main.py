from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.responses import ORJSONResponse
from app.middleware import register_middleware
from app.services.bootstrap import bootstrap_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    bootstrap_data()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

register_middleware(app)
app.include_router(api_router)


@app.get("/", tags=["root"])
def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "docs": "/docs",
    }
