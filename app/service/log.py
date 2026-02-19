from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select, and_, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.datastore.db import get_postgres_session
from app.core.enum import LogType
from app.core.utils.logs import get_calculate_func
from app.models.employee import Employee
from app.models.employee_logs import employees_logs_table
from app.models.log import Log
from app.service.base import BaseService


def get_log_service(
        session: AsyncSession = Depends(get_postgres_session)
):
    return LogService(session, Log)


class LogService(BaseService):

    async def get_logs_per_period(
            self,
            period,
            employee: Employee,
            log: Log
    ):
        query = (
            select(self.model).
            where(self.model.type == LogType.work_day).
            join(employees_logs_table).
            filter(
                and_(
                    employees_logs_table.c.employee_id == employee,
                    extract("year", self.model.date) == log.date.year,
                    extract("month", self.model.date) == log.date.month
                )
            ).
            order_by(self.model.date)
        )
        result = await self.session.execute(query)
        records = result.scalars().all()
        return records

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