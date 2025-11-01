from datetime import datetime, timezone, timedelta, date
from pydantic import BaseModel, computed_field

from app.core.enum import LogType




class WorkspaceCreate(BaseModel):
    name: str


class Employee(BaseModel):
    name: str
    surname: str | None = None
    fathers_name: str | None = None

    position: str | None = None
    vacation_time: int | None = None
    vacation_surplus: int | None = None
    days_off: int | None = None
    overwork_time: int | None = None
    sick_days: int | None = None


class LogCreate(BaseModel):
    type: LogType = LogType.work_day
    created_at: datetime = datetime.now(timezone.utc)
    log_date: date = date.today()

    # fields for periodic params of Log
    # day_start: date | None = None
    # day_end: date | None = None


    time_worked: int | None = None


    employees_id: list[int] = []


class LogResponse(BaseModel):
    type: LogType
    created_at: datetime
    log_date: date

    employees: list[Employee]


class WorkspaceResponse(WorkspaceCreate):
    employees: list[Employee]
    logs: list[LogCreate]


