from fastapi import FastAPI

from app.db.db import lifespan
from app.api.auth import router as auth

app = FastAPI(
    lifespan=lifespan
)

app.include_router(auth.router)


@app.get("/")
async def main():
    return {"message": "Hello World"}