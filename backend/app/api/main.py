from fastapi import APIRouter

from app.api.v1.routes import local, passengers, stats
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(passengers.router)
api_router.include_router(stats.router)
api_router.include_router(local.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(local.router)
