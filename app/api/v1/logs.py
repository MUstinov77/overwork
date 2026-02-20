from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.core.auth.request_validators import authenticate_user
from app.core.exceptions import NotFoundException
from app.core.utils.logs import calculate_employee_stats
from app.models.employee import Employee
from app.models.log import Log
from app.schemas.log import LogCreateUpdate, LogRetrieve
from app.service.employee import EmployeeService, get_employee_service
from app.service.log import LogService, get_log_service

router = APIRouter(
    dependencies=(
        Depends(authenticate_user,),
    ),
    prefix="/logs",
    tags=["logs"],
)


@router.get("/{employee_id}")
async def get_logs(
        employee_id: int,
        log_service: Annotated[LogService, Depends(get_log_service)],
):
    log = await log_service.retrieve_one(Log.id, 13)
    logs = await log_service.get_logs_data_per_period("month", employee_id, log)
    return logs


@router.get(
    "/{log_id}",
    response_model=LogRetrieve,
)
async def get_log_by_id(
        log_id: int,
        logs_service: Annotated[LogService, Depends(get_log_service)]
):
        log = await logs_service.retrieve_one(Log.id, log_id)
        if not log:
            raise NotFoundException
        return log


@router.post(
    "/",
    response_model=LogRetrieve,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def create_log(
        data: LogCreateUpdate,
        log_service: Annotated[LogService, Depends(get_log_service)],
        employee_service: Annotated[EmployeeService, Depends(get_employee_service)]
):
    log_data = data.model_dump()
    employees_id = log_data.pop("employees_id")
    log = await log_service.create_instance(log_data)
    if not log:
        raise NotFoundException
    for employee_id in employees_id:
        employee = await employee_service.retrieve_one(Employee.id, employee_id)
        employee.logs.append(log)
        try:
            await calculate_employee_stats(
                employee.statistics,
                log,
                "create",
                log_service
            )
        except ValueError:
            print("Error while changing employee stats")
    return log


@router.delete(
    "/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_log():
    pass


@router.patch(
    "/{log_id}",
    response_model=LogRetrieve,
)
async def update_log_by_id(updated_data: LogCreateUpdate):
    pass


