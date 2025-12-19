from datetime import date, datetime, timezone

from pydantic import BaseModel, computed_field

from app.core.enum import LogType


class WorkspaceCreate(BaseModel):
    name: str

class StatisticsRequest(BaseModel):
    vacation: int | None = None
    vacation_surplus: int | None = None
    days_off: int | None = None
    overwork_time: int | None = None
    sick_days: int | None = None

class EmployeeRequest(BaseModel):
    name: str
    surname: str | None = None
    fathers_name: str | None = None

    position: str | None = None



class EmployeeResponse(BaseModel):
    name: str | None = None
    surname: str | None = None
    fathers_name: str | None = None

    position: str | None = None
    vacation: int | None = None
    vacation_surplus: int | None = None
    days_off: int | None = None
    work_time: int | None = None
    overwork_time: int | None = None
    sick_days: int | None = None



class LogCreate(BaseModel):
    type: LogType = LogType.work_day
    log_date: date = date.today()

    data: int | None = None

    employees_id: list[int] = []


class WorkspaceResponse(WorkspaceCreate):
    employees: list[EmployeeResponse]
    logs: list[LogCreate]


class LogResponse(BaseModel):
    type: LogType
    created_at: datetime
    log_date: date
    data: int | None = None
    employees: list[EmployeeResponse]


