from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import select

from .schemas import WorkspaceCreate
from app.db.db import session_provider
from app.db.models import Workspace

router = APIRouter(
    prefix="/workspaces"
)

@router.get(
    "/",
    response_model=list[WorkspaceCreate])
async def get_my_workspaces(
        session: Depends(session_provider)
):
    workspaces = session.execute(select(Workspace)).scalars().all()
    return workspaces


@router.get("/{workspace_name}")
async def get_workspace_by_name(
        workspaces_name: str,
):
    return {
        "workspace": "workspace"
    }

@router.post("/")
async def create_workspace(
    data: WorkspaceCreate,
    session: Depends(session_provider)
):
    workspace = Workspace(**data.model_dump())
    #workspace.user_id = user.id
    session.add(workspace)
