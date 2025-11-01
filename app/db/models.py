from datetime import datetime, timezone, date

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, Enum, DateTime, Table, Column, Date

from ._base import Base
from app.core.enum import LogType


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String())

    workspaces: Mapped[list["Workspace"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Workspace(Base):

    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="workspaces")

    logs: Mapped[list["Log"]] = relationship(
        back_populates="workspace",
        cascade="all, delete-orphan",
    )
    employees: Mapped[list["Employee"]] = relationship(
        back_populates="workspace",
        cascade="all, delete-orphan",
    )

employees_logs_table = Table(
    "employees_logs",
    Base.metadata,
    Column(
        "employee_id",
        ForeignKey(
            "employees.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
    Column(
        "log_id",
        ForeignKey(
            "logs.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
)



class Employee(Base):

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String())
    surname: Mapped[str] = mapped_column(String(), nullable=True)
    fathers_name: Mapped[str] = mapped_column(String(), nullable=True)

    position: Mapped[str] = mapped_column(String(), nullable=True)

    # base stats for work day
    overwork_time: Mapped[int] = mapped_column(nullable=True)
    time_worked: Mapped[int] = mapped_column(nullable=True)

    # periodic attrs
    sick_days: Mapped[int] = mapped_column(nullable=True)
    vacation_time: Mapped[int] = mapped_column(nullable=True)
    vacation_surplus: Mapped[int] = mapped_column(nullable=True)
    days_off: Mapped[int] = mapped_column(nullable=True)

    workspace: Mapped[Workspace] = relationship(back_populates="employees")
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))

    logs: Mapped[list["Log"]] = relationship(
        secondary=employees_logs_table,
        back_populates="employees",
        cascade="all, delete",
    )


class Log(Base):

    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[str] = mapped_column(Enum(LogType))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc)
    )

    log_date: Mapped[date] = mapped_column(Date())

    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    workspace: Mapped["Workspace"] = relationship(back_populates="logs")

    employees: Mapped[list["Employee"]] = relationship(
        secondary=employees_logs_table,
        back_populates="logs",
        passive_deletes=True,
    )
