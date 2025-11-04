from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import DATABASE_URL


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSession = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_sqlite_db() -> None:
    """Create the DB and initialize tables as defined in the Base.metadata"""
    db_path = engine.url.database
    if not Path(db_path).exists():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
