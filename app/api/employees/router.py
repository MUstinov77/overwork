from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.datastore.db import session_provider
from app.core.exceptions import NotFoundException
from app.core.utils.db_queries import get_log_by_id
from app.core.utils.logs import change_employee_data_via_log
from app.models.employee import Employee
from app.models.log import Log
from app.schemas.employee import EmployeeCreateRetrieve, EmployeeUpdate
from app.schemas.log import LogCreateUpdate, LogRetrieve
from app.service.employee import EmployeeService, get_employee_service

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
    response_model=list[LogRetrieve]
)
async def get_employee_logs(
        employee: Annotated[Employee, Depends(get_employee_by_id)],
):
    return employee.logs


@router.post(
    "/{employee_id}/logs",
    response_model=LogRetrieve,
    status_code=status.HTTP_201_CREATED
)
async def create_log_via_employee(
        data: LogCreateUpdate,
        employee: Annotated[Employee, Depends(get_employee_by_id)],
        session: Annotated[Session, Depends(session_provider)],
):
    log_data = data.model_dump(exclude={"employees_id"})
    log = Log(**log_data)
    employee.workspace.logs.append(log)
    employee.logs.append(log)
    employee_stats = employee.statistics
    await change_employee_data_via_log(
        employee_stats,
        log,
        "create",
        session
    )
    return log


@router.get(
    "/{employee_id}/logs/{log_id}",
    response_model=LogRetrieve,
)
async def get_log_by_employee_id(
        log: Annotated[Log, Depends(get_log_by_id)],
):
    return log


@router.delete(
    "/{employee_id}/logs/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_employee_log(
        employee: Annotated[Employee, Depends(get_employee_by_id)],
        log: Annotated[Log, Depends(get_log_by_id)],
        session: Annotated[Session, Depends(session_provider)]
):
    employee.logs.remove(log)
    await change_employee_data_via_log(
        employee.statistics,
        log,
        "delete"
    )
    if not log.employees:
        session.delete(log)
    return log
