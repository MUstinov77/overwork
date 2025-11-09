from datetime import datetime, timezone, date
from pydantic import BaseModel

from app.core.enum import LogType




class WorkspaceCreate(BaseModel):
    name: str


class Employee(BaseModel):
    name: str
    surname: str | None = None
    fathers_name: str | None = None

    position: str | None = None
    vacation: int | None = None
    vacation_surplus: int | None = None
    days_off: int | None = None
    overwork_time: int | None = None
    sick_days: int | None = None


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


