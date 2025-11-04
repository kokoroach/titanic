from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = "sqlite+aiosqlite:///titanic.db"


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


def init_sqlite_db() -> None:
    """Create the DB and initialize tables as defined in the Base.metadata"""
    db_path = engine.url.database
    if not Path(db_path).exists():
        Base.metadata.create_all(bind=engine)
