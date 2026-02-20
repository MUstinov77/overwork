from sqlalchemy.orm import Session

from app.models.log import Log
from app.models.statistics import Statistics
from app.service.employee import EmployeeService


async def calculate_employee_stats(
        employee_stats: Statistics,
        # period,
        log: Log,
        action: str,
        log_service
):
    funcs_by_field = {
        "sick_day":calculate_sick_days,
        "vacation":calculate_vacation_surplus,
        "day_off": calculate_days_off,
        "work_day":calculate_overwork_time,
    }
    calculate_func = funcs_by_field.get(log.type.name, None)
    if not calculate_func:
        raise ValueError("Field not found")
    if log.data:
        await calculate_overwork_time(
            employee_stats,
            # period,
            log,
            action,
            log_service
        )
    await calculate_func(
        employee_stats,
        # period,
        log,
        action,
        log_service
    )
    return None


async def calculate_sick_days(
        employee_stats: Statistics,
        # period,
        action: str,
) -> None:
    match action:
        case "create":
            employee_stats.sick_days += 1
        case "delete":
            employee_stats.sick_days -= 1
        case _:
            raise ValueError("Action not found")
    return None


async def calculate_vacation_surplus(
        employee_stats: Statistics,
        # period,
        action: str,
) -> None:
    match action:
        case "create":
            employee_stats.vacation_surplus -= 1
        case "delete":
            employee_stats.vacation += 1
        case _:
            raise ValueError("Action not found")
    return None


async def calculate_days_off(
        employee_stats: Statistics,
        # period,
        action: str,
) -> None:
    match action:
        case "create":
            employee_stats.days_off += 1
        case "delete":
            employee_stats.days_off -= 1
        case _:
            raise ValueError("Action not found")
    return None

async def calculate_overwork_time(
        employee_stats: Statistics,
        # period,
        log: Log,
        action: str,
        log_service
) -> None:
    data = log.data or 8
    match action:
        case "create":
            work_time_per_month = await log_service.get_logs_data_per_period(
                # period,
                employee_stats.employee_id,
                log,
            )
            if work_time_per_month > 164:
                if (
                    employee_stats.overwork_updated_date.year == log.date.year and
                    employee_stats.overwork_updated_date.month == log.date.month
                ):
                    employee_stats.overwork_time += data
                else:
                    employee_stats.overwork_time += work_time_per_month - 164
                employee_stats.overwork_updated_date = log.date
        case "delete":
            employee_stats.overwork_time -= data
        case _:
            raise ValueError("Action not found")
