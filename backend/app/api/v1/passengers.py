from typing import Dict, List

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.application.passenger_service import upload_from_csv
from app.core.cache import (
    delete_keys_having_prefix,
    get_data_from_cache,
    set_cache_data,
)
from app.core.logging import logger
from app.db.passenger import get_all_passengers, get_passenger_by_id

PASSENGER_PREFIX = "passenger"


router = APIRouter()


@router.post("/upload-csv", status_code=200)
async def upload_csv(file: UploadFile = File(...)):
    """
    Endpoint that allows upload of Titanic's Passenger csv data.
    It will be serialized and stored in DB for further processing.

    The csv must follow the header as set in Kaggle dataset:
    https://www.kaggle.com/c/titanic/data?select=train.csv
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    print('HEREEE A')
    try:
        inserted_passengers = await upload_from_csv(file)
    except Exception:
        logger.error("Encountered some issue.", exc_info=True)
        raise HTTPException(
            status_code=400, detail="Server encountered an unexpected issue."
        )

    if inserted_passengers:
        # Reset cache if new data were inserted in the DB
        await delete_keys_having_prefix(prefix=PASSENGER_PREFIX)


@router.get("/", status_code=200)
async def get_passengers() -> List[dict]:
    """Return all of the Titanic passenger data"""
    redis_key = f"{PASSENGER_PREFIX}:all"

    cached_data = await get_data_from_cache(redis_key)
    if cached_data:
        return cached_data

    passengers = await get_all_passengers()
    passengers: List[Dict] = [p.to_dict() for p in passengers]

    # Set cache data
    await set_cache_data(redis_key, passengers)

    return passengers


@router.get("/{p_id}", status_code=200)
async def get_passenger(p_id: int):
    """Return a Titanic passenger"""
    redis_key = f"{PASSENGER_PREFIX}:{p_id}"

    # Check cache
    cached_data = await get_data_from_cache(redis_key)
    if cached_data:
        return cached_data

    passenger = await get_passenger_by_id(p_id)
    p = passenger.to_dict()

    # Set cache data
    await set_cache_data(redis_key, p)

    return p
