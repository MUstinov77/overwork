from app.service.base import BaseService
from app.models.user import User

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.datastore.db import get_postgres_session


def get_user_service(
        session: AsyncSession = Depends(get_postgres_session)
):
    return UserService(session, User)


class UserService(BaseService):
    pass