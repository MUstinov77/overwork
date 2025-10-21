from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.schemas import WorkspaceCreate
from app.db.db import session_provider
from app.db.models import Workspace, User
from app.core.utils.auth import get_current_user

router = APIRouter(
    prefix="/workspaces"
)

@router.get(
    "/",
    response_model=list[WorkspaceCreate])
async def get_my_workspaces(
        user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(session_provider)
):
    query = select(Workspace).where(Workspace.user_id == user.id)
    workspaces = session.execute(query).scalars().all()
    return workspaces


@router.get("/{workspace_name}")
async def get_workspace_by_name(
        workspaces_name: str,
):
    return {
        "workspace": "workspace"
    }

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