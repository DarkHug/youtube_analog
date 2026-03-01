from fastapi import APIRouter, Depends
import app.services.cache_service as cache_service

from app.infrastructure.redis_client import get_redis

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/redis_check")
async def check_redis(redis=Depends(get_redis)):
    await redis.ping()
    return {"message": "Redis is working"}


@router.get("/get_key")
async def get_key(key: str, redis=Depends(get_redis)):
    value = await cache_service.get(redis, key)
    if value is None:
        return {"message": f"Key '{key}' not found"}
    return {"key": key, "value": value}


@router.post("/set_key")
async def set_key(key: str, value: dict, redis=Depends(get_redis)):
    await cache_service.set(redis, key, value, ttl=10)
    return {"message": f"Key '{key}' set to '{value}'"}


@router.delete("/delete_key")
async def delete_key(key: str, redis=Depends(get_redis)):
    await cache_service.delete(redis, key)
    return {"message": f"Key '{key}' deleted"}
