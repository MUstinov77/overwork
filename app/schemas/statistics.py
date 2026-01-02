from pydantic import BaseModel


class StatisticsSchema(BaseModel):

    overwork_time: int | None = 0
    sick_days: int | None = 0
    vacation: int | None = 0
    vacation_surplus: int | None = 0
    days_off: int | None = 0