from csv import DictReader
from fastapi import APIRouter, UploadFile, File, HTTPException
from io import StringIO

from app.db.passenger import bulk_insert_passengers
from app.domain.exceptions import DataValidationError
from app.domain.passenger import Passenger


router = APIRouter()


@router.post("/upload-csv", status_code=200)
async def upload_csv(file: UploadFile = File(...)) -> None:
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

    validated_passengers = []
    for row in reader:
        try:
            p = await Passenger.from_dict(row)
            validated_passengers.append(p.as_json())
        except DataValidationError as e:
            raise e

    try:
        await bulk_insert_passengers(validated_passengers)
    except Exception as e:
        # TODO: Use verbose logging tool
        print('Error', e)
