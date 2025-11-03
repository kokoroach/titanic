from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = "sqlite:///titanic.db"


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def init_sqlite_db() -> None:
    """Create the DB and initialize tables as defined in the Base.metadata"""
    db_path = engine.url.database
    if not Path(db_path).exists():
        Base.metadata.create_all(bind=engine)
