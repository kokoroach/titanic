from sqlalchemy import func, select, text
from app.db.database import AsyncSession
from app.db.models import PassengerModel


async def get_numeric_passenger_stats(column):
    _column = text(column)
    async with AsyncSession() as session:
        stmt = select(
            func.min(_column),
            func.max(_column),
            func.avg(_column),
            func.count(_column)
        ).select_from(PassengerModel)

        result = await session.execute(stmt)
        stats_query = result.one()

        return {
            "type": "numeric",
            "min": float(stats_query[0]) if stats_query[0] is not None else None,
            "max": float(stats_query[1]) if stats_query[1] is not None else None,
            "avg": float(stats_query[2]) if stats_query[2] is not None else None,
            "count": stats_query[3],
        }


async def get_nonnumeric_passenger_stats(column):
    _column = text(column)
    async with AsyncSession() as session:
        stmt = (
            select(_column, func.count(_column))
            .group_by(_column)
            .order_by(func.count(_column).desc())
        ).select_from(PassengerModel)

        result = await session.execute(stmt)
        rows = result.all()

        return {
            "type": "categorical",
            "values": [{"value": r[0], "count": r[1]} for r in rows],
            "unique_count": len(rows)
        }
