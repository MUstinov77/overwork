from pydantic import BaseModel

from app.schemas.statistics import StatisticsSchema


class EmployeeCreateRetrieve(BaseModel):
    name: str
    surname: str | None = None
    fathers_name: str | None = None
    position: str | None = None
    #statistics: StatisticsSchema


class EmployeeUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    fathers_name: str | None = None
    position: str | None = None
