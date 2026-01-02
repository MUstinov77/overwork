from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.core.utils.auth import get_current_user
from app.core.utils.db_queries import (
    get_employee_by_id,
    get_log_by_id,
    get_workspace
    )
from app.core.utils.logs import change_employee_data_via_log
from app.core.datastore.db import session_provider
from app.models.log import Log
from app.models.workspace import Workspace
from app.schemas.log import LogCreateUpdate, LogRetrieve

router = APIRouter(
    dependencies=(
        Depends(get_current_user),
    ),
    tags=["logs"],
)


@router.get(
    "/",
    response_model=list[LogRetrieve],
    response_model_exclude_none=True,
)
async def get_logs(
        workspace: Annotated[Workspace, Depends(get_workspace)]
):
    return workspace.logs


@router.get(
    "/{log_id}",
    response_model=LogRetrieve,
)
async def get_logs_by_id(
        log: Annotated[Log, Depends(get_log_by_id)]
):
    return log


@router.post(
    "/",
    response_model=LogRetrieve,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    tags=["workspaces_logs"],
)
async def create_log(
    data: LogCreateUpdate,
    workspace: Annotated[Workspace, Depends(get_workspace)],
):
    log_data = data.model_dump(
        exclude_none=True,
        exclude_unset=True
    )
    employees_ids = log_data.pop("employees_id") or None
    if not employees_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Log should have at last one employee id"
        )
    log = Log(**log_data)
    workspace.logs.append(log)
    attr_name, data = log.type.name, log.data
    for employee_id in employees_ids:
        employee = get_employee_by_id(employee_id)
        employee.logs.append(log)
        await change_employee_data_via_log(
            employee.statistics,
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
        session: Annotated[Session, Depends(session_provider)],
):
    for employee in log.employees:
        await change_employee_data_via_log(
            employee.statistics,
            log.type.name,
            log.data,
            "delete"
        )
    session.delete(log)
    return


@router.patch(
    "/{log_id}",
    response_model=LogRetrieve,
)
async def update_log_by_id(
        updated_data: LogCreateUpdate,
        log: Annotated[Log, Depends(get_logs_by_id)],
        session: Annotated[Session, Depends(session_provider)],
):
    old_log_type, old_log_data = log.type.name, log.data
    updated_data = updated_data.model_dump(exclude_none=True)
    employees_ids = updated_data.pop("employees_id") or None
    session.execute(update(Log).where(Log.id == log.id).values(**updated_data))
    for employee in log.employees:
        await change_employee_data_via_log(
            employee.statistics,
            old_log_type,
            old_log_data,
            "delete"
        )
        await change_employee_data_via_log(
            employee.statistics,
            log.type.name,
            log.data,
            "create"
        )
    if employees_ids:
        for employee_id in employees_ids:
            employee = get_employee_by_id(employee_id)
            if employee not in log.employees:
                log.employees.append(employee)
                await change_employee_data_via_log(
                    employee.statistics,
                    log.type.name,
                    log.data,
                    "create"
                )
    return log
