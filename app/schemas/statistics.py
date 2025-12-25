from pydantic import BaseModel


class StatisticsSchema(BaseModel):

    overwork_time: int | None = None
    sick_days: int | None = None
    vacation: int | None = None
    vacation_surplus: int | None = None
    days_off: int | None = None