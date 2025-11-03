from sqlalchemy.dialects.sqlite import insert
from app.db.models import PassengerModel

from app.db.database import get_session


session = get_session()


async def bulk_insert_passengers(rows):
    stmt = insert(PassengerModel).values(rows)
    stmt = stmt.on_conflict_do_nothing(index_elements=["passenger_id"])
    session.execute(stmt)
    session.commit()
