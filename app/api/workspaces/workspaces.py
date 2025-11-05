from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.employees.router import router as employees_router
from app.api.schemas import WorkspaceCreate
from app.core.enum import RouterType
from app.db.db import session_provider
from app.db.models import Workspace, User
from app.core.utils.db_querys import get_workspace
from app.api.logs.router import router as logs_router
from app.core.utils.auth import get_current_user


router = APIRouter(
    prefix="/workspaces",
    tags=["workspaces"],
)

router.include_router(employees_router)
router.include_router(
    logs_router,
    prefix="/{workspace_name}/logs",
)


@router.get(
    "/",
    response_model=list[WorkspaceCreate]
)
async def get_my_workspaces(
        user: Annotated[User, Depends(get_current_user)],
):

    return user.workspaces


@router.get(
    "/{workspace_name}",
    response_model=WorkspaceCreate
)
async def get_workspace_by_name(
        workspace: Annotated[Workspace, Depends(get_workspace)]
):
    return workspace


@router.post(
    "/",
    response_model=WorkspaceCreate
)
async def create_workspace(
    data: WorkspaceCreate,
    user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(session_provider),

):
    workspace = Workspace(**data.model_dump())
    workspace.user_id = user.id
    session.add(workspace)
    return workspace


@router.delete("/{workspace_name}")
async def delete_workspace_by_name(
        workspace: Annotated[Workspace, Depends(get_workspace)],
        session: Session = Depends(session_provider)
):
    session.delete(workspace)
    return {"message": "Workspace deleted"}
