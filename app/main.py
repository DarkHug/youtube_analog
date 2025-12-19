from fastapi import FastAPI
from app.api.v1.auth_routes import router
# The variable name here must match the command string ':app'
app = FastAPI()

app.include_router(router)
@app.get("/")
async def root():
    return {"message": "Hello World"}