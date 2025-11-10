from typing import Dict

from sqlalchemy.sql.sqltypes import Float, Integer, Numeric, SmallInteger

from app.db.models import PassengerModel
from app.db.stats import get_nonnumeric_passenger_stats, get_numeric_passenger_stats


async def get_passenger_stats_by_data_point(column: str) -> Dict:
    """
    Retrieve statistical information for a specific data column (i.e. data
    point) in the passenger dataset.

    This function determines whether the requested column contains numeric or
    categorical data and returns the appropriate statistical metrics:
    """
    # Check if column exists
    _column = getattr(PassengerModel, column, None)
    if not _column:
        raise ValueError(
            f"Data point '{column}' not found in {PassengerModel.__tablename__}"
        )

    # Ignore id and names
    excluded_patterns = ["name", "alias", "spouse"]
    if column == "passenger_id" or any(p in column for p in excluded_patterns):
        raise ValueError(f"Data point '{column}' cannot be use for stats.")

    numeric_types = (Integer, Float, Numeric, SmallInteger)
    # Handle different data point metrics by type
    if isinstance(_column.type, numeric_types):
        stats = await get_numeric_passenger_stats(column)
        result = {
            "type": "numeric",
            "min": float(stats[0]) if stats[0] is not None else None,
            "max": float(stats[1]) if stats[1] is not None else None,
            "avg": float(stats[2]) if stats[2] is not None else None,
            "count": stats[3],
        }
    else:
        stats = await get_nonnumeric_passenger_stats(column)
        result = {
            "type": "categorical",
            "values": [{"value": r[0], "count": r[1]} for r in stats],
            "unique_count": len(stats),
        }
    return result
