from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.datastore.db import get_postgres_session
from app.models.employee import Employee
from app.models.log import Log
from app.models.employee_logs import employees_logs_table
from sqlalchemy import select
from app.service.base import BaseService
from app.core.utils.logs import get_calculate_func


def get_log_service(
        session: AsyncSession = Depends(get_postgres_session)
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

    async def get_logs_per_month(
            self,
            employee: Employee,
    ):
        # result = self.session.execute(
        #     select(Log).
        #     where(Log.type == LogType.work_day).
        #     join(employees_logs_table).
        #     filter(
        #         and_(
        #             employees_logs_table.c.employee_id == employee.id,
        #             extract("year", Log.date) == log.date.year,
        #             extract("month", Log.date) == log.date.month
        #         )
        #     ).
        #     order_by(Log.date)
        # ).scalars().all()
        pass