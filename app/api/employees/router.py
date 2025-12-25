from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.core.utils.db_querys import (
    get_employee_by_id,
    get_log_by_id,
    get_workspace
    )
from app.db.db import session_provider
from app.models.employee import Employee
from app.models.statistics import Statistics
from app.models.workspace import Workspace
from app.models.log import Log

from app.schemas.employee import EmployeeCreateUpdate, EmployeeRetrieve
from app.schemas.log import LogCreateUpdate, LogRetrieve

router = APIRouter(
    prefix="/{workspace_id}/employees",
    tags=["employees"],
)


@router.get(
    "/",
    response_model=list[EmployeeRetrieve],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Workspace not found"},
    }
)
async def get_workspace_employees(
        workspace: Annotated[Workspace, Depends(get_workspace)]
):
    if not workspace:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Workspace not found"})
    return workspace.employees


@router.get(
    "/{employee_id}",
    response_model=EmployeeRetrieve,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Employee not found"},
    }
)
async def get_employee_by_id(
        employee: Annotated[Employee, Depends(get_employee_by_id)],
):
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return employee

@router.get(
    "/{employee_id}/logs",
    response_model=list[LogRetrieve]
)
async def get_employee_logs(
        employee: Annotated[Employee, Depends(get_employee_by_id)],
):
    return employee.logs


@router.get(
    "/{employee_id}/logs/{log_id}",
    response_model=LogRetrieve,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Invalid request"}
    }
)
async def get_log_by_employee_id(
        employee: Annotated[Employee, Depends(get_employee_by_id)],
        log: Annotated[Log, Depends(get_log_by_id)],
):
    if not log or not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return log

@router.delete(
    "/{employee_id}/logs/{log_id}",
)
async def delete_employee_log(
        employee: Annotated[Employee, Depends(get_employee_by_id)],
        log: Annotated[Log, Depends(get_log_by_id)],
        session: Annotated[Session, Depends(session_provider)]
):
    employee.logs.remove(log)
    if not log.employees:
        session.delete(log)
    return {"message": "Log deleted"}

@router.post(
    "/",
    response_model=EmployeeRetrieve,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Workspace not found"},
        status.HTTP_409_CONFLICT: {"description": "Employee already exists"},
    },
)
async def create_employee(
        data: EmployeeCreateUpdate,
        workspace: Annotated[Workspace, Depends(get_workspace)],
):
    if not workspace:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Workspace not found"}
        )

    employee_data = data.model_dump(
        exclude_none=True
    )
    employee = Employee(**employee_data)
    employee.statistics = Statistics()
    workspace.employees.append(employee)
    return employee


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Employee not found"}
    })
async def delete_employee(
        employee: Annotated[Employee, Depends(get_employee_by_id)],
        workspace: Annotated[Workspace, Depends(get_workspace)],
        session: Annotated[Session, Depends(session_provider)]
):
    if not workspace or not employee:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Invalid employee or workspace"}
        )
    session.delete(employee)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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
