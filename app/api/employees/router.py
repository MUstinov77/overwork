from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.core.utils.logs import get_calculate_func
from app.models.employee import Employee
from app.models.log import Log
from app.schemas.employee import EmployeeCreateRetrieve, EmployeeUpdate
from app.schemas.log import LogCreateUpdate, LogRetrieve
from app.service.employee import EmployeeService, get_employee_service
from app.service.log import LogService, get_log_service

router = APIRouter(
    prefix="/{workspace_id}/employees",
    tags=["employees"],
)


@router.get(
    "/",
    response_model=list[EmployeeCreateRetrieve],
)
async def get_workspace_employees(
        workspace_id: int,
        employee_service: Annotated[EmployeeService, Depends(get_employee_service)]
):
    employees = await employee_service.retrieve_all(
        employee_service.model.workspace_id,
        workspace_id
    )
    if not employees:
        raise NotFoundException
    return employees


@router.get(
    "/{employee_id}",
    response_model=EmployeeCreateRetrieve,
)
async def get_employee_by_id(
        workspace_id : int,
        employee_id: int,
        employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
):
    employee = await employee_service.retrieve_one(
        employee_service.model.id,
        employee_id
    )
    if not employee:
        raise NotFoundException
    return employee


@router.post(
    "/",
    response_model=EmployeeCreateRetrieve,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee(
        workspace_id: int,
        data: EmployeeCreateRetrieve,
        employee_service: Annotated[EmployeeService, Depends(get_employee_service)]
):
    employee_data = data.model_dump(
        exclude_none=True
    )
    employee_data["workspace_id"] = workspace_id
    employee = await employee_service.create_instance(employee_data)
    return employee


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_employee(
        workspace_id: int,
        employee_id: int,
        employee_service: Annotated[EmployeeService, Depends(get_employee_service)]
):
    await employee_service.delete_instance(employee_id)
    return {"message": "Employee deleted"}


@router.patch(
    "/{employee_id}",
    response_model=EmployeeCreateRetrieve
)
async def update_employee(
        workspace_id: int,
        employee_id: int,
        data: EmployeeUpdate,
        employee_service: Annotated[EmployeeService, Depends(get_employee_service)]
):

    updated_data = data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )
    employee = await employee_service.update_instance(updated_data, employee_id)
    return employee


@router.get(
    "/{employee_id}/logs",
    response_model=list[LogRetrieve],
)
async def get_employee_logs(
        workspace_id: int,
        employee_id: int,
        log_service: Annotated[LogService, Depends(get_log_service)]
):
    logs = await log_service.retrieve_all(Employee.id, employee_id)
    if not logs:
        raise NotFoundException
    return logs


# @router.post(
#     "/{employee_id}/logs",
#     response_model=LogRetrieve,
#     status_code=status.HTTP_201_CREATED
# )
# async def create_log_via_employee(
#         data: LogCreateUpdate,
#         employee: Annotated[Employee, Depends(get_employee_by_id)],
#         session: Annotated[Session, Depends(session_provider)],
# ):
#     log_data = data.model_dump(exclude={"employees_id"})
#     log = Log(**log_data)
#     employee.workspace.logs.append(log)
#     employee.logs.append(log)
#     employee_stats = employee.statistics
#     await change_employee_data_via_log(
#         employee_stats,
#         log,
#         "create",
#         session
#     )
#     return log


@router.post(
    "/{employee_id}/logs",
    response_model=LogRetrieve,
    status_code=status.HTTP_201_CREATED
)
async def create_log_via_employee(
        data: LogCreateUpdate,
        workspace_id: int,
        employee_id: int,
        employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
        log_service: Annotated[LogService, Depends(get_log_service)]
):
    log_create_data = data.model_dump()
    log_create_data.pop("employees_id")
    log_create_data["workspace_id"] = workspace_id
    employee = await employee_service.retrieve_one(
        Employee.id,
        employee_id
    )
    log = await log_service.create_instance(log_create_data, employee)
    return log


@router.get(
    "/{employee_id}/logs/{log_id}",
    response_model=LogRetrieve
)
async def get_log_by_employee_id(
        workspace_id: int,
        employee_id: int,
        log_id: int,
        log_service: Annotated[LogService, Depends(get_log_service)],
):
    log = await log_service.retrieve_one(Log.id, log_id)
    if not log:
        return NotFoundException
    return log


@router.delete(
    "/{employee_id}/logs/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_employee_log(
        workspace_id: int,
        employee_id: int,
        log_id: int,
        employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
        log_service: Annotated[LogService, Depends(get_log_service)],
):
    employee = await employee_service.retrieve_one(Employee.id, employee_id)
    log = await log_service.delete_instance(log_id, employee)
    if not employee or not log:
        raise NotFoundException
    return log
