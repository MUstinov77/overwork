from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.employees.router import router as employees_router
from app.api.logs.router import router as logs_router
from app.core.auth.request_validators import authenticate_user
from app.core.exceptions import NotFoundException
from app.models.user import User
from app.schemas.workspace import WorkspaceCreateUpdate, WorkspaceRetrieve
from app.service.workspace import WorkspaceService, get_workspace_service

router = APIRouter(
    dependencies=(
        Depends(authenticate_user),
    ),
    prefix="/workspaces",
    tags=["workspaces"],
)

router.include_router(employees_router)
router.include_router(
    logs_router,
    prefix="/{workspace_id}/logs",
)


@router.get(
    "/",
    response_model=list[WorkspaceRetrieve],
)
async def get_my_workspaces(
        workspace_service: Annotated[WorkspaceService, Depends(get_workspace_service)]
):
    workspaces = await workspace_service.retrieve_all(
        workspace_service.model.user_id,
        7
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
    workspace_service: Annotated[WorkspaceService, Depends(get_workspace_service)],
):
    user = None
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
        data: WorkspaceCreateUpdate,
        workspace_id: int,
        workspace_service: Annotated[WorkspaceService, Depends(get_workspace_service)]
):
    updated_data = data.model_dump(
        exclude_none=True,
        exclude_unset=True,
    )
    workspace = await workspace_service.update_instance(updated_data, workspace_id)
    return workspace
