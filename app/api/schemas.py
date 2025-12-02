from datetime import date, datetime, timezone

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.core.enum import LogType


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


class EmployeeResponse(EmployeeRequest):
    pass


class LogCreate(BaseModel):
    type: LogType = LogType.work_time
    log_date: date = date.today()

    time_worked: int | None = None

    employees_id: list[int] = []


class WorkspaceResponse(WorkspaceCreate):
    employees: list[EmployeeResponse]
    logs: list[LogCreate]


class LogResponse(BaseModel):
    type: LogType
    created_at: datetime
    log_date: date
    time_worked: int | None = None
    employees: list[EmployeeResponse]