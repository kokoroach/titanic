from fastapi import APIRouter, HTTPException

from app.application.stats_service import get_passenger_stats_by_data_point
from app.core.cache import get_data_from_cache, set_cache_data

STATS_PREFIX = "passenger:stats"


router = APIRouter()


@router.get("/{column}", status_code=200)
async def get_numeric_passenger_stats(column: str):
    redis_key = f"{STATS_PREFIX}:{column}"

    # Check cache
    cached_data = await get_data_from_cache(redis_key)
    if cached_data:
        return cached_data

    try:
        stats = await get_passenger_stats_by_data_point(column)
    except Exception:
        raise HTTPException(
            status_code=400, detail="Server encountered an unexpected issue."
        )
    # Set cache data
    await set_cache_data(redis_key, stats)

    return stats
