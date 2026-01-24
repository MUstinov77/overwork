from sqlalchemy.orm import Session

from app.models.log import Log
from app.models.statistics import Statistics


def get_calculate_func(log_field_type):
    funcs_by_field = {
        "sick_day":calculate_sick_days,
        "vacation":calculate_vacation_surplus,
        "day_off": calculate_days_off,
        "work_day":calculate_overwork_time,
    }
    calculate_func = funcs_by_field.get(log_field_type, None)
    if not calculate_func:
        raise ValueError("Field not found")
    return calculate_func


def calculate_sick_days(
        employee_stats: Statistics,
        action: str,
        data: int | None = None
):
    match action:
        case "create":
            employee_stats.sick_days += 1
            if data:
                employee_stats.overwork_time += data
        case "delete":
            employee_stats.sick_days -= 1
            if data:
                employee_stats.overwork_time -= data
        case _:
            raise ValueError("Action not found")


def calculate_vacation_surplus(
        employee_stats: Statistics,
        action: str,
):
    match action:
        case "create":
            employee_stats.vacation_surplus -= 1
        case "delete":
            employee_stats.vacation += 1
        case _:
            raise ValueError("Action not found")


def calculate_days_off(
        employee_stats: Statistics,
        action: str,
        data: int | None = None
):
    match action:
        case "create":
            employee_stats.days_off += 1
            if data:
                employee_stats.overwork_time += data
        case "delete":
            employee_stats.days_off -= 1
            if data:
                employee_stats.overwork_time -= data
        case _:
            raise ValueError("Action not found")

def calculate_overwork_time(
        employee_stats: Statistics,
        log: Log,
        action: str,
        session: Session | None = None
):
    data = log.data or 8
    match action:
        case "create":
            get_logs_per_month = ...
            logs_per_month = get_logs_per_month(
                log,
                employee_stats.employee,
                session
            )
            if (
                employee_stats.overwork_updated_date is not None
                and
                employee_stats.overwork_updated_date.month == log.date.month
                and
                employee_stats.overwork_updated_date.year == log.date.year
            ):
                employee_stats.overwork_time += data
                employee_stats.overwork_updated_date = log.date
            else:
                overwork_time = data
                for month_log in logs_per_month:
                    overwork_time += month_log.data
                if overwork_time > 164:
                    employee_stats.overwork_time += overwork_time - 164
                    employee_stats.overwork_updated_date = log.date
        case "delete":
            employee_stats.overwork_time -= data
        case _:
            raise ValueError("Action not found")
