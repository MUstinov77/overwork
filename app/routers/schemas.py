from pydantic import BaseModel


class WorkspaceCreate(BaseModel):
    name: str


class Employee(BaseModel):
    name: str
    surname: str
    father_name: str | None = None

    position: str
    vacation_full: int
    vacation_surplus: int
    days_off: int
    overwork_time: int
    sick_days: int


class WorkspaceResponse(WorkspaceCreate):
    employees: list[Employee]
    logs: list[Log]
