import json


async def get(redis, key: str) -> dict | None:
    result = await redis.get(key)
    if result is None:
        return None
    return json.loads(result)


async def set(redis, key: str, value: dict, ttl) -> None:
    await redis.set(key, json.dumps(value), ex=ttl)


async def delete(redis, key: str) -> None:
    await redis.delete(key)
