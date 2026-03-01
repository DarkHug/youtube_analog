# Async Redis client
import asyncio
import redis.asyncio as redis

_redis: redis.Redis | None = None

async def init_redis(redis_url: str):
    global _redis
    client = redis.from_url(redis_url, decode_responses=True)
    await client.ping()
    _redis = client


def get_redis():
    if _redis is None:
        raise RuntimeError("redis not initialized")
    return _redis


async def close_redis():
    if _redis is not None:
        await _redis.close()
