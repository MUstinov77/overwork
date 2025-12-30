from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, extract
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.db.db import session_provider
from app.models.log import Log
from app.models.employee import Employee
from app.models.workspace import Workspace


def get_workspace(
    workspace_id: int,
    session: Session = Depends(session_provider),
):
    workspace = session.execute(
        select(Workspace).
        where(Workspace.id == workspace_id)
    ).scalar_one_or_none()
    if not workspace:
        raise NotFoundException
    return workspace


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

def get_logs_per_month(
        log,
        logs,
        session: Session = Depends(session_provider)
):
    result = session.execute(
        select(logs).
        filter(
            extract("year", Log.date) == log.date.year,
            extract("month", Log.date) == log.date.month
        )).all()
    return result

def get_employee_by_id(
        employee_id: int,
        session: Session = Depends(session_provider)
):
    employee = session.execute(
        select(Employee).
        where(Employee.id == employee_id)
    ).scalar_one_or_none()
    if not employee:
        raise NotFoundException
    return employee
