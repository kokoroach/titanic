import json
from typing import Any, Dict

import redis.asyncio as _redis
from redis.asyncio.client import Redis

from app.core.config import settings
from app.core.logging import logger

redis = None


async def get_redis() -> Redis:
    """Retrieve the active Redis client instance."""
    return redis


async def init_redis() -> None:
    """
    Initialize the Redis client connection using the configured `REDIS_URI`.

    Should be called on FastAPI application startup.
    """
    global redis
    redis = await _redis.from_url(
        str(settings.REDIS_URI), encoding="utf-8", decode_responses=True
    )
    logger.info("Redis is initialized...")


async def close_redis() -> None:
    """Close the Redis client connection."""
    redis = await get_redis()
    await redis.close()


async def delete_keys_having_prefix(prefix: str) -> None:
    """Delete all keys matching a given prefix."""
    redis = await get_redis()

    async for key in redis.scan_iter(match=f"{prefix}*"):
        await redis.delete(key)


async def get_data_from_cache(key: str) -> Dict | None:
    """Retrieve cached JSON data by key."""
    redis = await get_redis()
    cached = await redis.get(key)
    return json.loads(cached) if cached else None


async def set_cache_data(key: str, data: Any) -> None:
    """Store and serialize data to the Redis cache as JSON with expiration."""
    redis = await get_redis()
    await redis.set(key, json.dumps(data), ex=settings.REDIS_CACHE_TTL)
