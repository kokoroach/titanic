import json
from csv import DictReader
from fastapi import APIRouter, UploadFile, File, HTTPException
from io import StringIO
from typing import List, Dict

from app.core.logging import logger
from app.db.passenger import (
    bulk_insert_passengers,
    get_all_passengers,
    get_passenger_by_id
)
from app.core.cache import (
    get_redis,
    get_data_from_cache,
    delete_keys_having_prefix,
    set_cache_data
)


from app.domain.exceptions import DataValidationError
from app.domain.passenger import Passenger


PASSENGER_PREFIX = "passengers:"


router = APIRouter()


# Cache Interfaces


async def _invalidate_all_passenger_cache() -> None:
    await delete_keys_having_prefix(prefix=PASSENGER_PREFIX)



@router.post("/upload-csv", status_code=200)
async def upload_csv(file: UploadFile = File(...)):
    """
    Endpoint that allows upload of titanic's Passenger data in csv. It will be
    serialized and stored in DB for further processing.

    The csv data must follow the header as set in Kaggle dataset:
    https://www.kaggle.com/c/titanic/data?select=train.csv
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    contents = await file.read()
    buffer = StringIO(contents.decode('utf-8'))
    reader = DictReader(buffer)

    valid_passengers = []
    invalid_passengers = []
    for row in reader:
        try:
            # Inline data validation
            p = await Passenger.from_dict(row)
            valid_passengers.append(p.as_json())
        except DataValidationError:
            invalid_passengers.append(p)

    # Bulk insertion to database
    try:
        await bulk_insert_passengers(valid_passengers)
    except Exception as e:
        logger.error(f"API: Ran an issue when inserting passengers: {e}")
    finally:
        if invalid_passengers:
            logger.warning(
                "Found invalid/malformed passenger data: "
                f"{invalid_passengers}"
            )

    # Reset cache
    await _invalidate_all_passenger_cache()

@router.get("/all", status_code=200)
async def get_passengers() -> List[dict]:
    """Return all of the Titanic passenger data"""
    redis_key = f"{PASSENGER_PREFIX}:all"

    cached_data = await get_data_from_cache(redis_key)
    if cached_data:
        return cached_data

    _passengers = await get_all_passengers()
    passengers: List[Dict] = [p.to_dict() for p in _passengers]

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
