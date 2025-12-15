from sqlalchemy import ForeignKey, String, event
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.enum import LogType
from app.models.log import Log
from app.models.employee_logs import employees_logs_table



class Employee(Base):

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String())
    surname: Mapped[str] = mapped_column(String(), nullable=True)
    fathers_name: Mapped[str] = mapped_column(String(), nullable=True)

    position: Mapped[str] = mapped_column(String(), nullable=True)

    # base stats for work day
    overwork_time: Mapped[int] = mapped_column(nullable=True)
    work_time: Mapped[int] = mapped_column(nullable=True)

    # periodic attrs
    sick_days: Mapped[int] = mapped_column(nullable=True)
    vacation: Mapped[int] = mapped_column(nullable=True)
    vacation_surplus: Mapped[int] = mapped_column(nullable=True)
    days_off: Mapped[int] = mapped_column(nullable=True)
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
        passive_deletes=True,
    )


@event.listens_for(Employee.logs, "append")
def count_overwork(target, value, initiator):
    match value.type:
        case LogType.work_day:
            time_worked = value.data
            for log in target.logs[::-1]:
                if log.type == LogType.work_day and log.log_date.month == value.log_date.month:
                    time_worked += log.data
                    if time_worked > 164:
                        target.overwork_time = time_worked - 164
                else:
                    break
        case _:
            pass
