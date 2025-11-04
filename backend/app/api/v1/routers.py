from fastapi import APIRouter

from app.api.v1.passengers import router as passenger_router

VERSION = "v1"
router = APIRouter()


@router.get("/")
async def get_health() -> dict:
    # TODO: Include db_check in the health check
    return {"status": "OK"}


v1_routers = [
    (router, f"/{VERSION}/health", "Health Check"),
    (passenger_router, f"/{VERSION}/passengers", "Passenger"),
]
