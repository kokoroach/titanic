from asyncio import run
from core.config import TITANIC_DATASET
from domain.passenger import Passenger


async def init_dataset():
    passengers = await Passenger.from_csv(TITANIC_DATASET)
    print(passengers[0])


if __name__ == '__main__':
    run(init_dataset())
