from typing import Annotated
from datetime import timedelta

from sqlalchemy import update
from sqlalchemy.orm import Session
from fastapi import Depends

from app.core.enum import LogType
from app.api.schemas import LogCreate
from app.db.db import session_provider
from app.db.models import Employee


async def change_employee_data_via_log(
        employee: Employee,
        attr_name: str,
        session: Annotated[Session, Depends(session_provider)],
):
    funcs_by_field = {
        "sick_day": default_calculate_sum_of_params,
        "vacation": default_calculate_difference_of_params,
        "day_off": default_calculate_sum_of_params,
        "work_day": default_calculate_sum_of_params,
    }
    calculating_func = funcs_by_field.get(attr_name, default_calculate_sum_of_params)
    calculated_value = calculating_func(employee)


def default_calculate_sum_of_params(
        employee
):
    employee.sick_days += 1


def default_calculate_difference_of_params(
        employee_field_value,
        log_field_value,
):
    return employee_field_value - log_field_value

def calculate_sick_days(
        employee
):
    employee.sick_days += 1