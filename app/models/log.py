from datetime import date, datetime, timezone

from sqlalchemy import (
    TIMESTAMP,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    UniqueConstraint
    )
from sqlalchemy.dialects.postgresql import DATE
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enum import LogType
from app.models.base import Base
from app.models.employee_logs import employees_logs_table


class Log(Base):

    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[str] = mapped_column(Enum(LogType))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc)
    )

    date: Mapped[date] = mapped_column(DATE())
    data: Mapped[int] = mapped_column(nullable=True)

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey(
            "workspaces.id",
            ondelete="CASCADE"
        ),
    )
    workspace = relationship(
        "Workspace",
        back_populates="logs"
    )

    employees = relationship(
        "Employee",
        uselist=True,
        secondary=employees_logs_table,
        back_populates="logs",
    )