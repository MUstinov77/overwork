from typing import Annotated

from sqlalchemy import select, delete
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from app.db.db import session_provider
from app.core.utils.logs import change_employee_data_via_log
from app.core.utils.db_querys import get_workspace, get_employee_by_id, get_current_user, get_log_by_id

from app.db.models import Workspace, Employee, User, Log
from app.api.schemas import LogCreate



router = APIRouter(
    dependencies=(
        Depends(get_workspace),
        Depends(get_current_user),
    ),
    tags=["logs"],
)


@router.get(
    "/",
    response_model=list[LogCreate],

)
async def get_logs(
        workspace: Annotated[Workspace, Depends(get_workspace)]
):

    return workspace.logs


@router.get(
    "/{employee_id}",
    response_model=list[LogCreate]
)
async def get_logs_by_employee(
        employee: Annotated[Employee, Depends(get_employee_by_id)],
):
    return employee.logs


@router.post(
    "/",
    response_model=LogCreate,
    tags=["workspaces_logs"]
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


@router.delete(
    "/{log_id}",
    status_code=204
)
async def delete_log(
        log: Annotated[Log, Depends(get_log_by_id)],
        workspace: Annotated[Workspace, Depends(get_workspace)],
        session: Annotated[Session, Depends(session_provider)],
        change_data: bool = True,
        employees_ids: list[int] | None = None
):
    # workspace.logs.remove(log)
    session.delete(log)
    return {"message": "log deleted"}

