from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.api.employees.router import router as employees_router
from app.api.logs.router import router as logs_router
from app.core.exceptions import NotFoundException
from app.core.utils.auth import get_current_user
from app.core.utils.db_querys import get_workspace
from app.db.db import session_provider
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.workspace import WorkspaceCreateUpdate, WorkspaceRetrieve

router = APIRouter(
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
        user: Annotated[User, Depends(get_current_user)],
):
    return user.workspaces


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceRetrieve,
)
async def get_workspace_by_id(
        workspace: Annotated[Workspace, Depends(get_workspace)],
):
    return workspace


@router.post(
    "/",
    response_model=WorkspaceRetrieve,
    status_code=status.HTTP_201_CREATED,
)
async def create_workspace(
    data: WorkspaceCreateUpdate,
    user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(session_provider),
):
    workspace = Workspace(**data.model_dump())
    workspace.user_id = user.id
    session.add(workspace)
    session.commit()
    return workspace


@router.delete(
    "/{workspace_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_workspace_by_id(
        workspace: Annotated[Workspace, Depends(get_workspace)],
        session: Session = Depends(session_provider)
):
    session.delete(workspace)
    session.commit()
    return workspace


@router.patch(
    "/{workspace_id}",
    response_model=WorkspaceRetrieve
)
async def update_workspace(
        data: WorkspaceCreateUpdate,
        workspace: Annotated[Workspace, Depends(get_workspace)],
        session: Annotated[Session, Depends(session_provider)]
):
    session.execute(
        update(Workspace).where(Workspace.id == workspace.id).values(**data.model_dump())
    )
    session.commit()
    return workspace
