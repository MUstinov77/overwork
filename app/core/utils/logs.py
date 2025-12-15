from app.models.employee import Employee


async def change_employee_data_via_log(
        employee: Employee,
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
        calculating_func(employee, action, data)
    except ValueError:
        return


def calculate_sick_days(
        employee: Employee,
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
        employee: Employee,
        action: str,
        data: int = 1
):
    data = data or 1
    match action:
        case "create":
            employee.vacation_surplus = employee.vacation - data
        case "delete":
            employee.vacation += 1
        case _:
            raise ValueError("Action not found")


def calculate_days_off(
        employee: Employee,
        action: str,
        data: int = 1
):
    data = data or 1
    match action:
        case "create":
            employee.days_off += data
        case "delete":
            employee.days_off -= data
        case _:
            raise ValueError("Action not found")

def calculate_work_time(
        employee: Employee,
        action: str,
        data: int,
):
    data = data or 8
    match action:
        case "create":
            employee.work_time += data
        case "delete":
            employee.work_time -= data
        case _:
            raise ValueError("Action not found")