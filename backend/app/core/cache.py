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


async def delete_keys_with_prefix(redis: Redis, prefix: str):
    cursor = b'0'
    while cursor:
        cursor, keys = await redis.scan(cursor=cursor, match=f"{prefix}*", count=100)
        if keys:
            await redis.delete(*keys)