from fastapi import FastAPI

from app.api.workspaces.workspaces import router as workspaces_router
from app.db.db import lifespan
from app.api.auth.router import router as auth_router

app = FastAPI(
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(workspaces_router)


@app.get("/")
async def main():
    return {"message": "Hello World"}