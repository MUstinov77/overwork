from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.auth.request_validators import authenticate_user
from app.core.exceptions import NotFoundException
from app.models.user import User
from app.schemas.employee import EmployeeCreateRetrieve
from app.schemas.statistics import StatisticsSchema
from app.schemas.workspace import WorkspaceCreateUpdate, WorkspaceRetrieve
from app.service.employee import EmployeeService, get_employee_service
from app.service.statistics import StatisticsService, get_statistics_service
from app.service.workspace import WorkspaceService, get_workspace_service

router = APIRouter(
    dependencies=(
        Depends(authenticate_user),
    ),
    prefix="/workspaces",
    tags=["workspaces"],
)


@router.get(
    "/",
    response_model=list[WorkspaceRetrieve],
)
async def get_my_workspaces(
        user: Annotated[User, Depends(authenticate_user)],
        workspace_service: Annotated[WorkspaceService, Depends(get_workspace_service)]
):
    workspaces = await workspace_service.retrieve_all(
        workspace_service.model.user_id,
        user.id
    )
    if not workspaces:
        raise NotFoundException
    return workspaces

@router.get(
    "/{workspace_id}",
    response_model=WorkspaceRetrieve,
)
async def get_workspace_by_id(
        workspace_id: int,
        workspace_service: Annotated[WorkspaceService, Depends(get_workspace_service)],
):
    record = await workspace_service.retrieve_one(
        workspace_service.model.id,
        workspace_id
    )
    if not record:
        raise NotFoundException
    return record


@router.post(
    "/",
    response_model=WorkspaceRetrieve,
    status_code=status.HTTP_201_CREATED,
)
async def create_workspace(
    data: WorkspaceCreateUpdate,
    user: Annotated[User, Depends(authenticate_user)],
    workspace_service: Annotated[WorkspaceService, Depends(get_workspace_service)],
):
    create_data = data.model_dump()
    create_data["user_id"] = user.id
    workspace = await workspace_service.create_instance(create_data)
    return workspace


@router.delete(
    "/{workspace_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_workspace_by_id(
        workspace_id: int,
        workspace_service: Annotated[WorkspaceService, Depends(get_workspace_service)]
):
    workspace = await workspace_service.delete_instance(workspace_id)
    if not workspace:
        raise NotFoundException
    return workspace


@router.patch(
    "/{workspace_id}",
    response_model=WorkspaceRetrieve
)
async def update_workspace(
        workspace_id: int,
        data: WorkspaceCreateUpdate,
        workspace_service: Annotated[WorkspaceService, Depends(get_workspace_service)]
):
    updated_data = data.model_dump(
        exclude_none=True,
        exclude_unset=True,
    )
    workspace = await workspace_service.update_instance(updated_data, workspace_id)
    return workspace


@router.post(
    "/{workspace_id}/employees",
    response_model=EmployeeCreateRetrieve,
)
async def create_employee(
        workspace_id: int,
        employee_create_data: EmployeeCreateRetrieve,
        employee_service: Annotated[EmployeeService, Depends(get_employee_service)],
        statistics_service: Annotated[StatisticsService, Depends(get_statistics_service)]
):
    employee_data = employee_create_data.model_dump(
        exclude_none=True
    )
    stats_data = employee_data.pop("statistics", StatisticsSchema().model_dump())
    employee_data["workspace_id"] = workspace_id
    employee = await employee_service.create_instance(employee_data)
    stats_data["employee_id"] = employee.id
    _ = await statistics_service.create_instance(stats_data)
    return employee


@router.get(
    "/{workspace_id}/employees",
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