from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.datastore.db import session_provider
from app.models.workspace import Workspace
from app.service.base import BaseService


def get_workspace_service(
        session: Session = Depends(session_provider),
):
    return WorkspaceService(session, Workspace)


class WorkspaceService(BaseService):
    pass