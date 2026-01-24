from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.core.datastore.db import init_db, destroy_db
from app.api.auth.router import router as auth_router
from app.api.workspaces.router import router as workspace_router

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    try:
        yield
    finally:
        await destroy_db()

def create_app():

    app = FastAPI(
        title=settings.TITLE,
        lifespan=lifespan,
    )

    app.include_router(auth_router)
    #app.include_router(workspace_router)

    return app

