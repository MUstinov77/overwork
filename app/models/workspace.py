from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.employee import Employee
from app.models.log import Log
from app.models.base import Base


class Workspace(Base):

    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship(
        "User",
        back_populates="workspaces"
    )

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
