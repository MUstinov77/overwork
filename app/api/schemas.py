from datetime import datetime, timezone, date
from typing import Annotated

from pydantic import BaseModel

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from app.core.enum import LogType
from app.db.models import Employee as EmployeeModel
from app.core.utils.db_querys import get_employee_by_id


class WorkspaceCreate(BaseModel):
    name: str


class EmployeeRequest(BaseModel):
    name: str
    surname: str | None = None
    fathers_name: str | None = None

    position: str | None = None
    vacation: int | None = None
    vacation_surplus: int | None = None
    days_off: int | None = None
    overwork_time: int | None = None
    sick_days: int | None = None


class EmployeeResponse(BaseModel):
    pass


class LogCreate(BaseModel):
    type: LogType = LogType.work_time
    created_at: datetime = datetime.now(timezone.utc)
    log_date: date = date.today()

    # fields for periodic params of Log
    # day_start: date | None = None
    # day_end: date | None = None


    time_worked: int | None = None


    employees_id: list[int] = []


class WorkspaceResponse(WorkspaceCreate):
    employees: list[Employee]
    logs: list[LogCreate]


def get_employee_data(employee: Annotated[EmployeeModel, Depends(get_employee_by_id)]):
    data = Employee(**jsonable_encoder(employee))
    return data