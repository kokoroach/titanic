# from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import select, insert
from typing import List

from app.db.models import PassengerModel
from app.db.database import get_session, Session


session = get_session()


async def bulk_insert_passengers(passengers: List[dict]) -> None:
    """
    Utility function to bulk insert passengers into the DB. It ignores
    duplicate on the primary key "passenger_id"
    """
    with Session() as session:
        stmt = insert(PassengerModel).values(passengers)
        stmt = stmt.on_conflict_do_nothing(index_elements=["passenger_id"])
        session.execute(stmt)


async def get_all_passengers() -> List:
    """Returns all passenges as list of PassengerModel instance"""
    with Session() as session:
        stmt = select(PassengerModel)
        result = session.execute(stmt)
        passengers = result.scalars().all()
        return passengers
