from app.models.statistics import Statistics


async def change_employee_data_via_log(
        employee_stats: Statistics,
        attr_name: str,
        data: int,
        action: str = "create" or "delete",
):
    funcs_by_field = {
        "sick_day": calculate_sick_days,
        "vacation": calculate_vacation_surplus,
        "day_off": calculate_days_off,
        "work_day": calculate_work_time,
    }
    calculating_func = funcs_by_field.get(attr_name, None)
    if not calculating_func:
        raise ValueError("Field not found")
    try:
        calculating_func(employee_stats, action, data)
    except ValueError:
        return


def calculate_sick_days(
        employee: Statistics,
        action: str,
        data: int = 1
):
    data = data or 1
    match action:
        case "create":
            employee.sick_days += data
        case "delete":
            employee.sick_days -= data
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

def calculate_work_time(
        employee_stats: Statistics,
        action: str,
        data: int,
):
    data = data or 8
    match action:
        case "create":
            employee_stats.time_worked_per_month += data
        case "delete":
            employee_stats.time_worked_per_month -= data
        case _:
            raise ValueError("Action not found")