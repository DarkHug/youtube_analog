from fastapi import FastAPI
from app.api.v1.auth_routes import router as auth_router
from app.api.v1.channel_routes import router as channel_router
# The variable name here must match the command string ':app'
app = FastAPI()

app.include_router(auth_router)
app.include_router(channel_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}