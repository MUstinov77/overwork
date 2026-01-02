from sqlalchemy import ForeignKey, String, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enum import LogType
from app.models.base import Base
from app.models.employee_logs import employees_logs_table
from app.models.log import Log
from app.models.statistics import Statistics


class Employee(Base):

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String())
    surname: Mapped[str] = mapped_column(String(), nullable=True)
    fathers_name: Mapped[str] = mapped_column(String(), nullable=True)
    position: Mapped[str] = mapped_column(String(), nullable=True)

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey(
            "workspaces.id",
            ondelete="CASCADE"
        )
    )

    workspace = relationship(
        "Workspace",
        back_populates="employees"
    )
    logs = relationship(
        "Log",
        uselist=True,
        secondary=employees_logs_table,
        back_populates="employees",
        cascade="all, delete",
    )

    statistics = relationship(
        "Statistics",
        uselist=False,
        back_populates="employee",
        cascade="all, delete",
    )
