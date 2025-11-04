from sqlalchemy.sql.sqltypes import Integer, Float, Numeric, SmallInteger
from app.db.models import PassengerModel
from app.core.logging import logger
from app.db.stats import (
    get_nonnumeric_passenger_stats,
    get_numeric_passenger_stats
)


async def get_passenger_stats_by_data_point(column):
    # Check if column exists
    _column = getattr(PassengerModel, column, None)
    if not _column:
        raise ValueError(f"Data point '{column}' not found in {PassengerModel.__tablename__}")

    # Ignore id and names
    if (
        column == "passenger_id"
        or "name" in column
        or column in ["alias", "spouse"]
    ):
        raise ValueError(f"Data point '{column}' cannot be use for stats.")

    numeric_types = (Integer, Float, Numeric, SmallInteger)
    if isinstance(_column.type, numeric_types):
        result = await get_numeric_passenger_stats(column)
    else:
        result = await get_nonnumeric_passenger_stats(column)

    return result
