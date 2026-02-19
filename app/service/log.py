from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select, and_, extract
from sqlalchemy.sql.functions import sum
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

    # async def create_extract_via_period(self, period, log) -> list:
    #     year_extract = extract("year", self.model.date)
    #     match period:
    #         case "year":
    #             return [year_extract,]
    #         case "month":
    #             return [year_extract, extract("month", self.model.date)]
    #         case "week":
    #             return [
    #                 year_extract == log.date.year,
    #                 extract("month", self.model.date) == log.date.month,
    #                 extract("week", self.model.date) == log.date.week
    #             ]
    #         case _:
    #             raise ValueError("Invalid period")

    async def get_logs_data_per_period(
            self,
            # period,
            employee_id,
            log: Log
    ):
        query = (
            select(sum(self.model.data)).
            join(employees_logs_table, employees_logs_table.c.log_id == self.model.id).
            where(employees_logs_table.c.employee_id == employee_id).
            filter(
                and_(
                    extract("year", self.model.date) == log.date.year,
                    extract("month", self.model.date) == log.date.month,
                    # extract("week", self.model.date) == log.date.week
                )
            )
        )
        result = await self.session.execute(query)
        record = result.scalar()
        return record