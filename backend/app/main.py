from contextlib import asynccontextmanager
from fastapi import FastAPI
from uvicorn import run

from app.db.database import init_sqlite_db
from app.api.v1.routers import v1_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: Uses SQLITE for test purposes. NOT for production use.
    # Use appropriate DB initialization
    init_sqlite_db()
    yield
    # Graceful exit


app = FastAPI(lifespan=lifespan)

# Setup up versioned API routers
for router, prefix, tags in v1_routers:
    app.include_router(router, prefix=prefix, tags=tags)


if __name__ == '__main__':
    run(app, host="0.0.0.0", port=8000)
