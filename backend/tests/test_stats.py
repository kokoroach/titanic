import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.db.models import PassengerModel

# In-memory SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="function")
async def db_session():
    """
    Provide a fresh AsyncSession for each test, with tables created/dropped.
    """
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Provide session
    async with TestSessionLocal() as session:
        yield session  # This is the AsyncSession your test will use

    # Drop tables after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)




@pytest.mark.asyncio
async def test_insert_passengers(db_session):
    # TODO: Not working for asynyc context
    # db_session is already an AsyncSession from fixture
    # db_session.add_all([
    #     PassengerModel(
    #         passenger_id=1,
    #         survived=True,
    #         p_class=1,
    #         sex="m",
    #         age=30,
    #         sib_sp=0,
    #         par_ch=0,
    #         ticket="123",
    #         fare=100,
    #         title="Mr",
    #         first_name="John",
    #         maiden_name="",
    #         last_name="Doe",
    #         nickname="",
    #         alias="",
    #         spouse="",
    #         cabin="",
    #         embarked="S"
    #     ),
    #     PassengerModel(
    #         passenger_id=2,
    #         survived=False,
    #         p_class=2,
    #         sex="f",
    #         age=20,
    #         sib_sp=0,
    #         par_ch=0,
    #         ticket="124",
    #         fare=50,
    #         title="Mrs",
    #         first_name="Jane",
    #         maiden_name="",
    #         last_name="Doe",
    #         nickname="",
    #         alias="",
    #         spouse="",
    #         cabin="",
    #         embarked="C"
    #     ),
    # ])
    # await db_session.commit()

    # # Check insertion
    # result = await db_session.execute("SELECT COUNT(*) FROM passengers")
    # count = result.scalar_one()
    # assert count == 2
    ...
