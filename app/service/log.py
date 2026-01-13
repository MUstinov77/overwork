from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.datastore.db import session_provider
from app.schemas.statistics import StatisticsSchema
from app.models.employee import Employee
from app.models.log import Log
from app.models.statistics import Statistics
from app.service.base import BaseService
from app.core.utils.logs import get_calculate_func


def get_log_service(
        session: Annotated[Session, Depends(session_provider)]
):
    return LogService(session, Log)


class LogService(BaseService):

    async def create_instance(self, values: dict, employee: Employee | None = None):
        log = await super().create_instance(values)
        if not employee:
            self.session.rollback()
            raise HTTPException(
                status_code=400,
                detail="Employee is not found. Please provide valid employee id",
            )
        employee.logs.append(log)
        try:
            calculate_func = get_calculate_func(log.type.name)
            calculate_func(employee.statistics, "create", log.data)
            return log
        except ValueError:
            self.session.rollback()
            raise HTTPException(
                status_code=400,
                detail="Error while changing employee stats",
            )

    async def delete_instance(self, obj_id: int, employee: Employee | None = None):
        log = await super().delete_instance(obj_id)
        try:
            calculate_func = get_calculate_func(log.type.name)
            calculate_func(employee.statistics, "delete", log.data)
            return log
        except ValueError:
            self.session.rollback()
            raise HTTPException(
                status_code=400,
                detail="Error while changing employee stats",
            )