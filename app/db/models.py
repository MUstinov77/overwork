from datetime import datetime, timezone

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, Enum, DateTime, Table, Column

from ._base import Base
from app.core.enum import LogType


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String())

    workspaces: Mapped[list["Workspace"]] = relationship(back_populates="user")


class Workspace(Base):

    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="workspaces")

    logs: Mapped[list["Log"]] = relationship(back_populates="workspace")
    employees: Mapped[list["Employee"]] = relationship(back_populates="workspace")



employees_logs_table = Table(
    "employees_logs",
    Base.metadata,
    Column("employee_id", ForeignKey("employees.id"), primary_key=True),
    Column("log_id", ForeignKey("logs.id"), primary_key=True),
)

class Employee(Base):

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String())
    surname: Mapped[str] = mapped_column(String())
    fathers_name: Mapped[str] = mapped_column(String())

    position: Mapped[str] = mapped_column(String())
    overwork_time: Mapped[int] = mapped_column()
    sick_days: Mapped[int] = mapped_column()
    vacation_time: Mapped[int] = mapped_column()
    vacation_surplus: Mapped[int] = mapped_column()
    days_off: Mapped[int] = mapped_column()

    workspace: Mapped["Workspace"] = relationship(back_populates="employees")
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))

    logs: Mapped[list["Log"]] = relationship(
        secondary=employees_logs_table,
        back_populates="employees"
    )


class Log(Base):

    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[str] = mapped_column(Enum(LogType))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc)
    )

    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    workspace: Mapped["Workspace"] = relationship(back_populates="logs")

    employees: Mapped[list["Employee"]] = relationship(
        secondary=employees_logs_table,
        back_populates="logs"
    )

