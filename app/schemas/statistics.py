from pydantic import BaseModel


class StatisticsSchema(BaseModel):

    overwork_time: int | None
    sick_days: int | None
    vacation: int | None
    vacation_surplus: int | None
    days_off: int | None