"""
FastAPI Application Entry Point

This module sets up the FastAPI application with:
- Lifecycle management (startup/shutdown events)
- Middleware (CORS)
- Versioned API routers
- Database and Redis initialization

To run the app:
    uvicorn app.main:app --port 8001 --reload
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from app.api.main import api_router
from app.core.cache import close_redis, init_redis
from app.core.config import settings
from app.core.logging import logger
from app.db.database import init_sqlite_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Async context manager for FastAPI lifespan events.

    It handles tasks before the app starts and after it shuts down:
    """
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


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

if __name__ == "__main__":
    """
    Run the application using Uvicorn server.
    """
    run(app, host="0.0.0.0", port=8001)
