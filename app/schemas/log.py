from datetime import date as py_date

from pydantic import BaseModel

from app.core.enum import LogType
from app.schemas.employee import EmployeeCreateRetrieve


class LogBase(BaseModel):
    type: LogType = LogType.work_day
    date: py_date = py_date.today()
    data: int | None = None
    workspace_id: int


class LogCreateUpdate(LogBase):
    employees_id: list[int] = []


class LogRetrieve(LogBase):
    ...
    #employees: list[EmployeeCreateRetrieve]
