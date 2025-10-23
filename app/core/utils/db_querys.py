from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.db import session_provider
from app.core.utils.auth import get_current_user
from app.db.models import Workspace, User, Log, Employee



def get_workspace(
    workspace_name: str,
    user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(session_provider)
):
    return session.execute(
        select(Workspace).
        where(Workspace.name == workspace_name).
        where(Workspace.user == user)
    ).scalar_one_or_none()

def get_employee_by_id(
        employee_id: int,
        user: Annotated[User, Depends(get_current_user)],
        workspace: Annotated[Workspace, Depends(get_workspace)],
        session: Annotated[Session, Depends(session_provider)]
):
    return session.execute(
        select(Employee).
        where(Employee.id == employee_id).
        where(Employee.workspace == workspace)
    ).scalar_one_or_none()
