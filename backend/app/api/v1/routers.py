from fastapi import APIRouter

from app.api.v1.passengers import router as passengers_router
from app.api.v1.stats import router as stats_router

API_VERSION = "v1"
router = APIRouter()


@router.get("/")
async def get_health() -> dict:
    """Expose an endpoint that checks for system health"""
    # TODO: Include DB and cache layer
    return {"status": "OK"}


v1_routers = [
    (router, f"/{API_VERSION}/health", "Health Check"),
    (passengers_router, f"/{API_VERSION}/passengers", "Passenger"),
    (stats_router, f"/{API_VERSION}/passengers/stats", "Passenger Stats"),
]
