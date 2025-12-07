from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.schemas import LogCreate, LogResponse
from app.core.enum import LogType
from app.core.utils.db_querys import (
    get_current_user,
    get_employee_by_id,
    get_log_by_id,
    get_workspace
    )
from app.core.utils.logs import change_employee_data_via_log
from app.db.db import session_provider
from app.db.models import Log, User, Workspace

router = APIRouter(
    dependencies=(
        Depends(get_workspace),
        Depends(get_current_user),
    ),
    tags=["logs"],
)


@router.get(
    "/",
    response_model=list[LogResponse],
    response_model_exclude_none=True,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Workspace not found"}
    }
)
async def get_logs(
        workspace: Annotated[Workspace, Depends(get_workspace)]
):
    if not workspace:
        return JSONResponse(
            content={"message": "Workspace not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    if not workspace.logs:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Empty logs"}
        )
    return workspace.logs


@router.get(
    "/{log_id}",
    response_model=LogCreate,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Log not found"}
    }
)
async def get_logs_by_id(
        log: Annotated[Log, Depends(get_log_by_id)]
):
    if not log:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Log not found"}
        )
    return log


@router.post(
    "/",
    response_model=LogResponse,
    response_model_exclude_none=True,
    tags=["workspaces_logs"],
    responses={
        status.HTTP_400_BAD_REQUEST: {"message": "Log should get almost one employee id"}
    }
)
async def create_log(
    data: LogCreate,
    workspace: Annotated[Workspace, Depends(get_workspace)],
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(session_provider)],
):
    log_data = data.model_dump(
        exclude_none=True,
        exclude_unset=True
    )
    employees_ids = log_data.pop("employees_id") or None
    if not employees_ids:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Log should get almost one employee id"}
        )
    log = Log(**log_data)
    workspace.logs.append(log)
    attr_name, data = log.type.name, log.data
    for employee_id in employees_ids:
        employee = get_employee_by_id(
            employee_id,
            user,
            workspace,
            session
        )
        employee.logs.append(log)
        await change_employee_data_via_log(
            employee,
            attr_name,
            data,
            "create",
        )
    return log


@router.delete(
    "/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_log(
        log: Annotated[Log, Depends(get_log_by_id)],
        workspace: Annotated[Workspace, Depends(get_workspace)],
        session: Annotated[Session, Depends(session_provider)],
        employees_ids: list[int]
):
    for employee_id in employees_ids:
        employee = get_employee_by_id(
            employee_id,
            workspace.user,
            workspace,
            session
        )
        await change_employee_data_via_log(
            employee,
            log.type.name,
            "delete"
        )
        employee.logs.remove(log)
    if not log.employees:
        session.delete(log)
    return {"message": "log deleted"}


@router.patch(
    "/{log_id}"
)
async def update_log_by_id(
        log: Annotated[Log, Depends(get_logs_by_id)],
):
    pass