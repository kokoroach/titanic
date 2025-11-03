from contextlib import asynccontextmanager
from fastapi import FastAPI
from uvicorn import run
from typing import AsyncGenerator

from app.db.database import init_sqlite_db
from app.api.v1.routers import v1_routers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """system- and app- related checks before and after FastAPI is ran."""
    # TODO: Uses SQLite for test purposes
    # Use appropriate DB initialization. In this case, for SQLite
    init_sqlite_db()
    yield
    # Post-processes including graceful exit


app = FastAPI(lifespan=lifespan)

# Setup up versioned API routers
for router, prefix, tags in v1_routers:
    app.include_router(router, prefix=prefix, tags=tags)


if __name__ == '__main__':
    run(app, host="0.0.0.0", port=8000)
