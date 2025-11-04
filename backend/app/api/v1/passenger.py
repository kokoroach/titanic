import json
from csv import DictReader
from fastapi import APIRouter, UploadFile, File, HTTPException
from io import StringIO
from typing import List

from app.core.logging import logger
from app.db.passenger import (
    bulk_insert_passengers,
    get_all_passengers,
    get_passenger_by_id
)
from app.core.cache import get_redis, delete_keys_with_prefix, CACHE_TTL

from app.domain.exceptions import DataValidationError
from app.domain.passenger import Passenger


PASSENGER_PREFIX = "passengers:"


router = APIRouter()


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
    invalid_passenger = []
    for row in reader:
        try:
            p = await Passenger.from_dict(row)
            valid_passengers.append(p.as_json())
        except DataValidationError:
            invalid_passenger.append(p)

    try:
        await bulk_insert_passengers(valid_passengers)
    except Exception as e:
        logger.error(f"API: Ran an issue when inserting passengers: {e}")
    finally:
        if invalid_passenger:
            logger.warning(
                "Found invalid/malformed passenger data: "
                f"{invalid_passenger}"
            )

    # Invalidate all existing passenger cache
    redis = await get_redis()
    await delete_keys_with_prefix(redis=redis, prefix=PASSENGER_PREFIX)


@router.get("/all", status_code=200)
async def get_passengers() -> List[dict]:
    """Return all of the Titanic passenger data"""
    redis_key = f"{PASSENGER_PREFIX}:all"
    redis = await get_redis()

    # Check cache
    cached = await redis.get(redis_key)
    if cached:
        logger.info("Getting all passengers from cache.")
        return json.loads(cached)

    _passengers = await get_all_passengers()
    passengers = [p.to_dict() for p in _passengers]

    # Build cache
    await redis.set(redis_key, json.dumps(passengers), ex=CACHE_TTL)


@router.get("/{p_id}", status_code=200)
async def get_passenger(p_id: int):
    """Return a Titanic passenger"""
    redis_key = f"{PASSENGER_PREFIX}:{p_id}"
    redis = await get_redis()

    # Check cache
    cached = await redis.get(redis_key)
    if cached:
        logger.info("Getting all passengers from cache.")
        return json.loads(cached)

    passenger = await get_passenger_by_id(p_id)
    p = passenger.to_dict()

    # Build cache
    await redis.set(redis_key, json.dumps(p), ex=CACHE_TTL)

    return p
