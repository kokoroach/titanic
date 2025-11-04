import pytest

from app.core.config import TITANIC_DATASET
from app.domain.passenger import Passenger


@pytest.mark.asyncio
async def test_csv_ingestion():
    passengers = await Passenger.from_csv(TITANIC_DATASET)

    assert isinstance(passengers[0], Passenger)
