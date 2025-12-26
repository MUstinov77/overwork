from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.core.utils.auth import get_current_user
from app.db.db import session_provider
from app.models.employee import Employee
from app.models.log import Log
from app.models.user import User
from app.models.workspace import Workspace


def get_workspace(
    workspace_id: int,
    user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(session_provider),
):
    workspace = session.execute(
        select(Workspace).
        where(Workspace.id == workspace_id).
        where(Workspace.user == user)
    ).scalar_one_or_none()
    if not workspace:
        raise NotFoundException
    return workspace

def get_employee_by_id(
        employee_id: int,
        user: Annotated[User, Depends(get_current_user)],
        workspace: Annotated[Workspace, Depends(get_workspace)],
        session: Annotated[Session, Depends(session_provider)]
):
    employee = session.execute(
        select(Employee).
        where(Employee.id == employee_id).
        where(Employee.workspace == workspace)
    ).scalar_one_or_none()
    if not employee:
        raise NotFoundException
    return employee

def get_log_by_id(
        log_id: int,
        session: Annotated[Session, Depends(session_provider)]
):
    log = session.execute(
        select(Log).
        where(Log.id == log_id).
        join(Workspace.logs)
    ).scalar_one_or_none()
    if not log:
        raise NotFoundException
    return log

def get_employee_stats(
        employee: Employee,
):
    return employee.statistics