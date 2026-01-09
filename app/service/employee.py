from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.datastore.db import session_provider
from app.schemas.statistics import StatisticsSchema
from app.models.employee import Employee
from app.models.statistics import Statistics
from app.service.base import BaseService


def get_employee_service(
        session: Annotated[Session, Depends(session_provider)]
):
    return EmployeeService(session, Employee)


class EmployeeService(BaseService):

    async def create_instance(self, values: dict):
        employee_stats_data = values.pop("statistics", StatisticsSchema().model_dump())
        employee = await super().create_instance(values)
        employee_stats_data["employee_id"] = employee.id
        try:
            stats = Statistics(**employee_stats_data)
            self.session.add(stats)
            self.session.commit()
            return employee
        except SQLAlchemyError:
            self.session.rollback()
            raise HTTPException(
                status_code=400,
                detail="Error while creating employee",
            )
