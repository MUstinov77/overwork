from pydantic import BaseModel

from app.schemas.statistics import StatisticsSchema

class EmployeeCreateUpdate(BaseModel):
    name: str
    surname: str | None = None
    fathers_name: str | None = None
    position: str | None = None


class EmployeeRetrieve(EmployeeCreateUpdate):

    statistics: StatisticsSchema
