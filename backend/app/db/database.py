from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from typing import Annotated, Any


DATABASE_URL = "sqlite:///titanic.db"


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def init_sqlite_db() -> None:
    """TODO"""
    db_path = engine.url.database
    if not Path(db_path).exists():
        Base.metadata.create_all(bind=engine)


def get_session() -> Annotated[Any, "Running DB session"]:
    return session
