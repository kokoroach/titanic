from typing import List

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert

from app.core.logging import logger
from app.db.database import AsyncSession
from app.db.models import PassengerModel


async def bulk_insert_passengers(passengers: List[dict]) -> int:
    """
    Utility function to bulk insert passengers into the DB. It ignores
    duplicate on the primary key "passenger_id"
    """
    async with AsyncSession() as session:
        stmt = insert(PassengerModel).values(passengers)
        stmt = stmt.on_conflict_do_nothing(index_elements=["passenger_id"])
        result = await session.execute(stmt)
        await session.commit()

        inserted_rows = result.rowcount
        logger.info(f"Inserted {inserted_rows} passengers.")

        return inserted_rows


async def get_all_passengers() -> List[PassengerModel]:
    """Returns all passengers as list of PassengerModel instance"""
    passengers = []
    async with AsyncSession() as session:
        stmt = select(PassengerModel)
        result = await session.execute(stmt)
        passengers = result.scalars().all()
    return passengers


async def get_passenger_by_id(p_id: int) -> PassengerModel:
    async with AsyncSession() as session:
        stmt = select(PassengerModel).where(PassengerModel.passenger_id == p_id)
        result = await session.execute(stmt)
        passenger = result.scalars().first()
    return passenger
