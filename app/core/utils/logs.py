from sqlalchemy.orm import Session

from app.core.utils.db_queries import get_logs_per_month
from app.models.log import Log
from app.models.statistics import Statistics


async def change_employee_data_via_log(
        employee_stats: Statistics,
        log: Log,
        action: str = "create" or "delete",
        session: Session | None = None
):
    funcs_by_field = {
        "sick_day": calculate_sick_days,
        "vacation": calculate_vacation_surplus,
        "day_off": calculate_days_off,
        "work_day": calculate_overwork_time,
    }
    calculating_func = funcs_by_field.get(log.type.name, None)
    if not calculating_func:
        raise ValueError("Field not found")
    try:
        calculating_func(employee_stats, log, action, session)
    except ValueError:
        return


def calculate_sick_days(
        employee_stats: Statistics,
        action: str,
        data: int = 1
):
    data = data or 1
    match action:
        case "create":
            employee_stats.sick_days += data
        case "delete":
            employee_stats.sick_days -= data
        case _:
            raise ValueError("Action not found")


def calculate_vacation_surplus(
        employee_stats: Statistics,
        action: str,
        data: int = 1
):
    data = data or 1
    match action:
        case "create":
            employee_stats.vacation_surplus = employee_stats.vacation - data
        case "delete":
            employee_stats.vacation += 1
        case _:
            raise ValueError("Action not found")


def calculate_days_off(
        employee_stats: Statistics,
        action: str,
        data: int = 1
):
    data = data or 1
    match action:
        case "create":
            employee_stats.days_off += data
        case "delete":
            employee_stats.days_off -= data
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