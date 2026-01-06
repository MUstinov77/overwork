from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.datastore.db import session_provider
from app.models.user import User
from app.models.workspace import Workspace
from app.service.base import BaseService


def get_workspace_service(
        session: Session = Depends(session_provider),
):
    return WorkspaceService(session, Workspace)


class WorkspaceService(BaseService):

    async def retrieve_by_user(self, user: User):
        query = select(self.model).where(self.model.user == user)
        result = self.session.execute(query)
        return result.scalars().all()
