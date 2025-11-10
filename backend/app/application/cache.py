import json
from functools import wraps
from typing import Any, Callable, Coroutine, Dict

from app.core.cache import get_redis
from app.core.config import settings
from app.core.logging import logger


def cached(key_template: str, ttl: int = settings.REDIS_CACHE_TTL):
    """
    Async decorator to cache function results in Redis.

    Args:
        key_template: A key template with placeholders in `{}`.
        ttl: time-to-live in seconds for cache
    """

    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Resolve a Redis key template with placeholders in the form:
            # "base:{key1}:{key2}"
            key = key_template.format_map(kwargs)

            # Check cache
            cached_data = await get_data_from_cache(key)
            if cached_data is not None:
                logger.info(f"Returning cached data for key: {key}")
                return cached_data

            # Call original function
            result = await func(*args, **kwargs)

            # Save to cache
            await set_cache_data(key, result, ttl=ttl)
            return result

        return wrapper

    return decorator


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


async def set_cache_data(key: str, data: Any, ttl: int) -> None:
    """Store and serialize data to the Redis cache as JSON with expiration."""
    redis = await get_redis()
    await redis.set(key, json.dumps(data), ex=ttl)
