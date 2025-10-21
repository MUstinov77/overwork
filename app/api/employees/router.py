from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.utils.db_querys import get_workspace
from app.db.models import Workspace, Employee
from ..schemas import Employee as EmployeeSchema

router = APIRouter(
    prefix="/{workspace_name}/employees"
)

 # router.include_router() include log router here

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
