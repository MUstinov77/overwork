from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.datastore.db import get_postgres_session
from app.models.statistics import Statistics
from app.service.base import BaseService


def get_statistics_service(
        session: Annotated[AsyncSession, Depends(get_postgres_session)]
):
    return StatisticsService(session, Statistics)


class StatisticsService(BaseService):
    pass