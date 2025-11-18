from datetime import date, datetime, timezone

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.core.enum import LogType
from app.core.utils.db_querys import get_employee_by_id
from app.db.models import Employee as EmployeeModel


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

    time_worked: int | None = None

    employees_id: list[int] = []


class WorkspaceResponse(WorkspaceCreate):
    employees: list[EmployeeResponse]
    logs: list[LogCreate]
