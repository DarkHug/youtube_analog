from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.v1.auth_routes import router as auth_router
from app.api.v1.channel_routes import router as channel_router
from app.api.v1.video_routes import router as video_router
from app.api.v1.test_routes import router as test_router
from app.core.settings import settings
from app.infrastructure.redis_client import init_redis, close_redis


# The variable name here must match the command string ':app'
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Срабатывает при старте приложения
    await init_redis(settings.REDIS_URL)
    yield
    # 2. Срабатывает при выключении приложения
    await close_redis()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(channel_router)
app.include_router(video_router)
app.include_router(test_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
