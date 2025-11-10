import json
from typing import Any, Dict

from app.core.config import settings
from app.core.cache import get_redis


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
