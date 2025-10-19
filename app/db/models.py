from datetime import datetime, timezone

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, Enum, DateTime

from ._base import Base
from app.core.enum import LogType


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String())

    workspaces: Mapped[list["Workspace"]] = relationship(back_populates="user")


class Workspace(Base):

    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="workspace")

    logs: Mapped[list["Log"]] = relationship(back_populates="workspace")
    employees: Mapped[list["Employee"]] = relationship(back_populates="workspace")


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
    logs: Mapped[list["Log"]] = relationship(back_populates="employees")


class Log(Base):

    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[str] = mapped_column(Enum(LogType))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc)
    )

    employees: Mapped[list["Employee"]] = relationship(back_populates="logs")
    workspace: Mapped["Workspace"] = relationship(back_populates="logs")

