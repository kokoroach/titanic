from typing import List

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert

from app.db.models import PassengerModel
from app.db.database import Session


async def bulk_insert_passengers(passengers: List[dict]) -> None:
    """
    Utility function to bulk insert passengers into the DB. It ignores
    duplicate on the primary key "passenger_id"
    """
    with Session() as session:
        stmt = insert(PassengerModel).values(passengers)
        stmt = stmt.on_conflict_do_nothing(index_elements=["passenger_id"])
        session.execute(stmt)
        session.commit()


async def get_all_passengers() -> List[PassengerModel]:
    """Returns all passengers as list of PassengerModel instance"""
    passengers = []
    with Session() as session:
        stmt = select(PassengerModel)
        result = session.execute(stmt)
        passengers = result.scalars().all()
    return passengers


async def get_passenger_by_id(p_id: int) -> PassengerModel:
    with Session() as session:
        stmt = select(PassengerModel).where(
            PassengerModel.passenger_id == p_id
        )
        result = session.execute(stmt)
        passenger = result.scalars().first()
    return passenger
