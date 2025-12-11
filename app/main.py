from fastapi import FastAPI

# The variable name here must match the command string ':app'
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}