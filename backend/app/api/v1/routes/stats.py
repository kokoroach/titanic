from fastapi import APIRouter

from app.application.cache import cached
from app.application.service.stats_service import get_passenger_stats_by_data_point

STATS_REDIS_PREFIX = "passenger:stats"


router = APIRouter()


@router.get("/{column}", status_code=200)
@cached("stats:{column}")
async def get_passenger_stats(column: str):
    """
    Get the statistical data for a specified column for the Passenger.

    It does not work and will raise and error on unique identifies like
    passenger_id, first_name etc.
    """
    stats = await get_passenger_stats_by_data_point(column)
    return stats
