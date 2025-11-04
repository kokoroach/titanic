from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import AsyncGenerator
from uvicorn import run

from app.api.v1.routers import v1_routers
from app.db.database import init_sqlite_db
from app.core.logging import logger

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """system- and app- related checks before and after FastAPI is ran."""
    logger.info("Running pre-startup checks before running FastAPI")
    # TODO: Uses SQLite for test purposes
    # Use appropriate DB initialization. In this case, for SQLite
    init_sqlite_db()
    # TODO:
    # Run a migration check and update for updated models
    yield
    logger.info("Shutting down API application...")
    # Post-process checks including potential graceful exit


app = FastAPI(lifespan=lifespan)

# TODO: Test purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
)


# Setup up versioned API routers
for router, prefix, tags in v1_routers:
    app.include_router(router, prefix=f"/api{prefix}", tags=tags)


if __name__ == '__main__':
    run(app, host="0.0.0.0", port=8000)
