from fastapi import FastAPI

from app.api.auth.router import router as auth_router
from app.api.workspaces.router import router as workspaces_router
from app.core.datastore.db import lifespan

app = FastAPI(
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(workspaces_router)


@app.get("/")
async def main():
    return {"message": "Hello World"}