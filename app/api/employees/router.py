from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.core.utils.db_queries import (
    get_employee_by_id,
    get_log_by_id,
    get_workspace,
    get_logs_per_month
    )
from app.core.utils.logs import change_employee_data_via_log
from app.db.db import session_provider
from app.models.employee import Employee
from app.models.log import Log
from app.models.statistics import Statistics
from app.models.workspace import Workspace
from app.schemas.employee import EmployeeCreateUpdate, EmployeeRetrieve
from app.schemas.log import LogCreateUpdate, LogRetrieve

router = APIRouter(
    dependencies=(
        Depends(get_workspace),
    ),
    prefix="/{workspace_id}/employees",
    tags=["employees"],
)


@router.get(
    "/",
    response_model=list[EmployeeRetrieve],
)
async def get_workspace_employees(
        workspace: Annotated[Workspace, Depends(get_workspace)]
):
    return workspace.employees


@router.get(
    "/{employee_id}",
    response_model=EmployeeRetrieve,
)
async def get_employee_by_id(
        employee: Annotated[Employee, Depends(get_employee_by_id)],
):
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return employee


@router.post(
    "/",
    response_model=EmployeeRetrieve,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee(
        data: EmployeeCreateUpdate,
        session: Annotated[Session, Depends(session_provider)],
        workspace: Annotated[Workspace, Depends(get_workspace)]
):
    employee_data = data.model_dump(
        exclude_none=True
    )
    employee = Employee(**employee_data)
    employee.workspace_id = workspace.id
    stats = Statistics()
    employee.statistics = Statistics()
    # workspace.employees.append(employee)
    return employee


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_employee(
        employee: Annotated[Employee, Depends(get_employee_by_id)],
        session: Annotated[Session, Depends(session_provider)]
):
    session.delete(employee)
    return employee


@router.patch(
    "/{employee_id}",
    response_model=EmployeeRetrieve
)
async def update_employee(
        data: EmployeeCreateUpdate,
        employee: Annotated[Employee, Depends(get_employee_by_id)],
        session: Annotated[Session, Depends(session_provider)],
):

    updated_data = data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    session.execute(
        update(Employee).where(Employee.id == employee.id).values(**updated_data)
    )
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
