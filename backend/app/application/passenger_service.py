from csv import DictReader
from io import StringIO

from fastapi import File

from app.core.logging import logger
from app.db.passenger import bulk_insert_passengers
from app.domain.exceptions import DataValidationError
from app.domain.passenger import Passenger


async def upload_from_csv(file: File):
    inserted_passengers = 0

    valid_passengers = []
    invalid_passengers = []

    contents = await file.read()
    buffer = StringIO(contents.decode("utf-8"))
    reader = DictReader(buffer)

    for row in reader:
        try:
            # Inline data validation
            p = await Passenger.from_dict(row)
            valid_passengers.append(p.as_json())
        except DataValidationError:
            invalid_passengers.append(p)

    # Bulk insertion to database
    try:
        inserted_passengers = await bulk_insert_passengers(valid_passengers)
    except Exception as e:
        logger.error(f"API: Ran an issue when inserting passengers: {e}")
    finally:
        if invalid_passengers:
            logger.warning(
                "Found invalid/malformed passengers: " f"{invalid_passengers}"
            )
    return inserted_passengers
