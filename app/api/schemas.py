from datetime import datetime, timezone
from pydantic import BaseModel

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


class Log(BaseModel):
    type: LogType
    created_at: datetime = datetime.now(timezone.utc)
    employees: list[Employee] = []


class WorkspaceResponse(WorkspaceCreate):
    employees: list[Employee]
    logs: list[Log]
