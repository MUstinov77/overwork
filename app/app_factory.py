from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api_router
from app.core.config import get_settings
from app.core.datastore.db import destroy_db, init_db

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

    app.include_router(api_router)

    return app

