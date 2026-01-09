from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.datastore.db import session_provider
from app.models.employee import Employee
from app.models.statistics import Statistics
from app.service.base import BaseService


def get_employee_service(
        session: Annotated[Session, Depends(session_provider)]
):
    return EmployeeService(session, Employee)


class EmployeeService(BaseService):

    async def create(self, values: dict):
        employee_stats_data = values.pop("statistics")
        employee = self.model(**values)
        stats = Statistics(**employee_stats_data)
        employee.statistics = stats
        self.session.add(employee)
        self.session.commit()
        return employee

    async def delete_employee(self, employee_id: int):
        try:
            employee = await self.delete(employee_id)
            self.session.commit()
            return employee
        except SQLAlchemyError:
            self.session.rollback()
            raise HTTPException(
                status_code=400,
                detail="Error while deleting workspace",
            )


    async def retrieve_by_workspace(self, workspace_id: int):
        query = select(self.model).where(self.model.workspace_id == workspace_id)
        result = self.session.execute(query)
        return result.scalars().all()
