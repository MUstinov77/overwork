from datetime import date

from pydantic import BaseModel

from app.core.enum import LogType
from app.schemas.employee import EmployeeResponse


class LogBase(BaseModel):
    type: LogType = LogType.work_day
    date: date = date.today()
    data: int | None = None


class LogCreateUpdate(LogBase):
    employees_id: list[int] = []


class LogResponse(LogBase):

    employees: list[EmployeeResponse]