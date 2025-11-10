from typing import Dict, List

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.application.cache import cached, delete_keys_having_prefix
from app.application.service.passenger_service import upload_from_csv
from app.core.logging import logger
from app.db.passenger import get_all_passengers, get_passenger_by_id

router = APIRouter()


@router.post("/upload-csv", status_code=201)
async def upload_csv(file: UploadFile = File(...)):
    """
    Endpoint that allows upload of Titanic's Passenger csv data.
    It will be serialized and stored in DB for further processing.

    The csv must follow the header as set in Kaggle dataset:
    https://www.kaggle.com/c/titanic/data?select=train.csv
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    try:
        inserted_passengers = await upload_from_csv(file)
    except Exception:
        logger.error("Encountered some issue.", exc_info=True)
        raise HTTPException(
            status_code=400, detail="Server encountered an unexpected issue."
        )

    # Reset cache if new data are inserted in the DB
    if inserted_passengers:
        await delete_keys_having_prefix(prefix="passenger")


@router.get("/", status_code=200)
@cached("passenger:all")
async def get_passengers():
    """Return all of the titanic Passenger data"""
    # TODO: Implement pagination
    passengers = await get_all_passengers()
    passengers: List[Dict] = [p.to_dict() for p in passengers]
    return passengers


@router.get("/{pass_id}", status_code=200)
@cached("passenger:{pass_id}")
async def get_passenger(pass_id: int):
    """Return the specified Passenger by its ID."""
    passenger = await get_passenger_by_id(pass_id)
    p = passenger.to_dict()
    return p
