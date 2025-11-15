from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.api.employees.router import router as employees_router
from app.api.schemas import WorkspaceResponse, WorkspaceCreate
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
    prefix="/{workspace_id}/logs",
)


@router.get(
    "/",
    response_model=list[WorkspaceResponse],
    responses={404: {"description": "User not found"}}
)
async def get_my_workspaces(
        user: Annotated[User, Depends(get_current_user)],
):
    return user.workspaces if user else JSONResponse(status_code=404, content={"message": "User not found"})


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
    responses={404: {"description": "Workspace not found"}}
)
async def get_workspace_by_id(
        workspace: Annotated[Workspace, Depends(get_workspace)],
):
    if not workspace:
        return JSONResponse(status_code=404, content={"message": "Workspace not found"})
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


@router.delete(
    "/{workspace_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Workspace not found"}}
)
async def delete_workspace_by_id(
        workspace: Annotated[Workspace, Depends(get_workspace)],
        session: Session = Depends(session_provider)
):
    if workspace:
        session.delete(workspace)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(status_code=404, content={"message": "Workspace not found"})

@router.patch(
    "/{workspace_id}",
    response_model=WorkspaceCreate
)
async def update_workspace(
        data: WorkspaceCreate,
        workspace: Annotated[Workspace, Depends(get_workspace)],
        session: Annotated[Session, Depends(session_provider)]
):
    session.execute(
        update(Workspace).where(Workspace.id == workspace.id).values(**data.model_dump())
    )
    return workspace