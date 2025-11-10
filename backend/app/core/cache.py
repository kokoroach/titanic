import redis.asyncio as _redis
from redis.exceptions import ConnectionError
from redis.asyncio.client import Redis

from app.core.config import settings
from app.core.logging import logger

redis = None


async def _test_redis_connection():
    """Tests that redis connection is okay."""
    try:
        redis = await get_redis()
        await redis.ping()
        return True
    except ConnectionError as e:
        raise e


async def get_redis() -> Redis:
    """Retrieve the active Redis client instance."""
    return redis


async def init_redis() -> None:
    """Initialize the Redis client connection."""
    global redis
    redis = await _redis.from_url(
        str(settings.REDIS_URI), encoding="utf-8", decode_responses=True
    )

    assert await _test_redis_connection()
    logger.info("Redis is initialized...")


async def close_redis() -> None:
    """Close the Redis client connection."""
    redis = await get_redis()
    await redis.close()
    logger.info("Redis connection is closed...")
