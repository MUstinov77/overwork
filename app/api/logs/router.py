from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.db import session_provider
from app.core.utils.logs import change_employee_data_via_log
from app.core.utils.db_querys import get_workspace, get_employee_by_id, get_current_user

from app.db.models import Workspace, Employee, User, Log
from app.api.schemas import LogCreate, LogResponse



router = APIRouter(
    dependencies=(
        Depends(get_workspace),
        # Depends(get_employee_by_id),
        Depends(get_current_user),
    ),
    tags=["logs"],
)


@router.get(
    "/",
    response_model=list[LogResponse],
    tags=["workspaces_logs"]
)
async def get_workspace_logs(
    workspace: Annotated[Workspace, Depends(get_workspace)],
    #user: Annotated[User, Depends(get_current_user)],
):
    return workspace.logs

@router.post(
    "/",
    response_model=LogResponse,
    tags=["workspaces_logs"]
)
async def create_log_by_workspace(
    data: LogCreate,
    workspace: Annotated[Workspace, Depends(get_workspace)],
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(session_provider)]
):
    log_data = data.model_dump(
        exclude_none=True,
        exclude_unset=True
    )
    employees_ids = log_data.pop("employees_id")
    log = Log(**log_data)
    workspace.logs.append(log)
    for employee_id in employees_ids:
        employee = get_employee_by_id(employee_id, user, workspace, session)
        employee.logs.append(log)
        attr_name = log.type.name
        await change_employee_data_via_log(
            employee,
            attr_name,
            session
        )
    return log


@router.get(
    "/",
    response_model=list[LogCreate],
    tags=["employees_logs"]
)
async def get_logs(
    workspace: Annotated[Workspace, Depends(get_workspace)],
    #user: Annotated[User, Depends(get_current_user)],
    employee: Annotated[Employee, Depends(get_employee_by_id)]
):
    return employee.logs

@router.get(
    "/{log_id}",
    response_model=LogCreate,
    tags=["employees_logs"]
)
async def get_log_by_id(
    log_id: int,
    #user: Annotated[User, Depends(get_current_user)],
    employee: Annotated[Employee, Depends(get_employee_by_id)],
    workspace: Annotated[Workspace, Depends(get_workspace)]
):
    return employee.logs.filter(Log.id == log_id).one_or_none()
