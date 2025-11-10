from typing import List

from sqlalchemy import func, select, text
from sqlalchemy.engine.row import Row

from app.db.database import AsyncSession
from app.db.models import PassengerModel


async def get_numeric_passenger_stats(column) -> Row:
    """
    Retrieve numerical statistics for a given column in the PassengerModel.
    """
    _column = text(column)
    async with AsyncSession() as session:
        stmt = select(
            func.min(_column), func.max(_column), func.avg(_column), func.count(_column)
        ).select_from(PassengerModel)

        result = await session.execute(stmt)
        return result.one()


async def get_nonnumeric_passenger_stats(column) -> List[Row]:
    """
    Retrieve non-numerical statistics for a given column in the PassengerModel.
    """
    _column = text(column)
    async with AsyncSession() as session:
        stmt = (
            select(_column, func.count(_column))
            .group_by(_column)
            .order_by(func.count(_column).desc())
        ).select_from(PassengerModel)

        result = await session.execute(stmt)
        return result.all()
