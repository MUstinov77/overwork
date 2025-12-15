from datetime import date, datetime, timezone

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table
    )
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enum import LogType

from ._base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String())

    workspaces: Mapped[list["Workspace"]] = relationship(
        back_populates="user",
        cascade="all, delete",
    )


class Workspace(Base):

    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="workspaces")

    logs: Mapped[list["Log"]] = relationship(
        back_populates="workspace",
        cascade="all, delete",
        passive_deletes=True
    )
    employees: Mapped[list["Employee"]] = relationship(
        back_populates="workspace",
        cascade="all, delete",
        passive_deletes=True
    )

employees_logs_table = Table(
    "employees_logs",
    Base.metadata,
    Column(
        "employee_id",
        Integer,
        ForeignKey(
            "employees.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
    Column(
        "log_id",
        Integer,
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


    workspace: Mapped[Workspace] = relationship(back_populates="employees")
    logs: Mapped[list["Log"]] = relationship(
        secondary=employees_logs_table,
        back_populates="employees",
        cascade="all, delete",
        passive_deletes=True,
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
    data: Mapped[int] = mapped_column(nullable=True)

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey(
            "workspaces.id",
            ondelete="CASCADE"
        ),
    )
    workspace: Mapped["Workspace"] = relationship(
        "Workspace",
        back_populates="logs"
    )

    employees: Mapped[list["Employee"]] = relationship(
        secondary=employees_logs_table,
        back_populates="logs",
        passive_deletes=True,
    )
