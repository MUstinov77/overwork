from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.datastore.db import get_postgres_session
from app.models.employee import Employee
from app.models.statistics import Statistics
from app.schemas.statistics import StatisticsSchema
from app.service.base import BaseService


def get_employee_service(
        session: AsyncSession = Depends(get_postgres_session)
):
    return EmployeeService(session, Employee)


class EmployeeService(BaseService):

    pass
