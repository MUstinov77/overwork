from typing import Annotated

from sqlalchemy import update
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.core.utils.router_factory import get_logs_router
from app.db.db import session_provider
from app.core.utils.db_querys import get_workspace, get_employee_by_id
from app.db.models import Workspace, Employee
from ..schemas import Employee as EmployeeSchema
from ...core.enum import RouterType

router = APIRouter(
    prefix="/{workspace_name}/employees"
)

router.include_router(get_logs_router(RouterType.employees))

@router.get(
    "/",
    response_model=list[EmployeeSchema]
)
async def get_workspace_employees(
        workspace: Annotated[Workspace, Depends(get_workspace)]
):
    return workspace.employees


@router.post(
    "/",
    response_model=EmployeeSchema
)
async def create_employee(
        data: EmployeeSchema,
        workspace: Annotated[Workspace, Depends(get_workspace)],
):
    employee = Employee(**data.model_dump())
    employee.workspace_id = workspace.id
    workspace.employees.append(employee)
    return employee


@router.delete("/{employee_id}")
async def delete_employee(
        employee: Annotated[Employee, Depends(get_employee_by_id)],
        workspace: Annotated[Workspace, Depends(get_workspace)],
):
    workspace.employees.remove(employee)
    return {"message": "employee deleted"}


@router.patch(
    "/{employee_id}",
    response_model=EmployeeSchema
)
async def update_employee(
        employee_id: int,
        data: EmployeeSchema,
        employee: Annotated[Employee, Depends(get_employee_by_id)],
        workspace: Annotated[Workspace, Depends(get_workspace)],
        session: Annotated[Session, Depends(session_provider)]
):
    updated_data = data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    session.execute(
        update(Employee).where(Employee.id == employee_id).values(**updated_data)
    )
    return employee
