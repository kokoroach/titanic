import json
from typing import List, Any

import redis.asyncio as _redis
from redis.asyncio.client import Redis

from app.core.logging import logger


REDIS_URL = "redis://localhost:6379"
CACHE_TTL = 600  # 10 mins

redis = None


async def get_redis() -> Redis:
    return redis


async def init_redis():
    global redis
    redis = await _redis.from_url(
        REDIS_URL,
        encoding="utf-8",
        decode_responses=True
    )
    logger.info("Redis is initialized...")


async def close_redis():
    redis = await get_redis()
    await redis.close()


async def delete_keys_having_prefix(prefix: str):
    redis = await get_redis()
    cursor = b'0'
    while cursor:
        cursor, keys = await redis.scan(
            cursor=cursor,
            match=f"{prefix}*",
            count=100
        )
        if keys:
            await redis.delete(*keys)


async def get_data_from_cache(key: str) -> dict | None:
    redis = await get_redis()
    cached = await redis.get(key)
    return json.loads(cached) if cached else None


async def set_cache_data(key: str, data: Any) -> None:
    redis = await get_redis()
    await redis.set(key, json.dumps(data), ex=CACHE_TTL)
