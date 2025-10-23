from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.db import session_provider
from app.core.utils.db_querys import get_workspace, get_employee_by_id, get_current_user
from ..enum import RouterType
from app.db.models import Workspace, Employee, User, Log
from app.api.schemas import Log


def get_logs_router(router_type: RouterType):
    router = APIRouter(
        dependencies=(
            Depends(get_workspace),
            # Depends(get_employee_by_id),
            Depends(get_current_user),
        ),
        prefix="/{workspace_name}/logs" if router_type == RouterType.workspaces else "/{employee_id}/logs",
    )

    if router_type == RouterType.workspaces:

        @router.get("/")
        async def get_logs(
                workspace: Annotated[Workspace, Depends(get_workspace)],
                user: Annotated[User, Depends(get_current_user)],
        ):
            return workspace.logs

        @router.post(
            "/",
            response_model=Log
        )
        async def create_log(
                data: Log,
                workspace: Annotated[Workspace, Depends(get_workspace)],
                user: Annotated[User, Depends(get_current_user)],
                employees_ids: Annotated[list[int], Query()],
                session: Annotated[Session, Depends(session_provider)]
        ):
            log = Log(**data.model_dump())

            # for employee_id in employees_ids:
                # employee = get_employee_by_id(employee_id, user, workspace, session)
                # employee.logs.append(log
            # )
            # add append via association_table(Logs, employees)
            workspace.logs.append(log)
            return log


    elif router_type.employees:

        @router.get(
            "/",
            response_model=list[Log])
        async def get_logs(
                workspace: Annotated[Workspace, Depends(get_workspace)],
                user: Annotated[User, Depends(get_current_user)],
                employee: Annotated[Employee, Depends(get_employee_by_id)]
        ):
            return employee.logs


        @router.get(
            "/{log_id}",
            response_model=Log
        )
        async def get_log_id(
                log_id: int,
                user: Annotated[User, Depends(get_current_user)],
                employee: Annotated[Employee, Depends(get_employee_by_id)],
                workspace: Annotated[Workspace, Depends(get_workspace)]
        ):
            return employee.logs.filter(Log.id == log_id).one_or_none()


    return router