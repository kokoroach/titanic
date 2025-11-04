from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from app.api.v1.routers import v1_routers
from app.core.cache import close_redis, init_redis
from app.core.config import ALLOWED_ORIGINS
from app.core.logging import logger
from app.db.database import init_sqlite_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """system- and app- related checks before and after FastAPI is ran."""
    logger.info("Running pre-startup checks before running FastAPI")
    # TODO: Uses SQLite for test purposes
    # Use appropriate DB initialization. In this case, for SQLite
    await init_sqlite_db()
    await init_redis()
    # TODO:
    # Run a migration check and update for updated models
    yield
    logger.info("Shutting down API application...")
    # Post-process checks including potential graceful exit
    await close_redis()


app = FastAPI(lifespan=lifespan)

# TODO: Test purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
)


# Setup up versioned API routers
for router, prefix, tags in v1_routers:
    app.include_router(router, prefix=f"/api{prefix}", tags=tags)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8001)
