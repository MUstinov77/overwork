from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
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

    async def delete_workspace(self, workspace_id: int):
        try:
            workspace = await self.delete(workspace_id)
            self.session.commit()
            return workspace
        except SQLAlchemyError:
            self.session.rollback()
            raise HTTPException(
                status_code=400,
                detail="Error while deleting workspace",
            )

    async def retrieve_by_user(self, user: User):
        query = select(self.model).where(self.model.user == user)
        result = self.session.execute(query)
        return result.scalars().all()
