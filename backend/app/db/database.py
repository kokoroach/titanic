from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings
from app.core.logging import logger

# Create an asynchronous SQLAlchemy engine. Example for aiosqlite engine
engine = create_async_engine(str(settings.SQLALCHEMY_SQLITE_DB_URI), echo=True)
AsyncSession = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    All models should inherit from this Base
    """

    pass


async def _assert_db_connection():
    """Checks that DB connection is okay."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        raise e


async def init_db() -> None:
    """Initialize DB connection"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    assert await _assert_db_connection()
    logger.info("Database initialized...")


async def close_db() -> None:
    """Close DB connection"""
    await engine.dispose()
    print("Database connection closed...")
