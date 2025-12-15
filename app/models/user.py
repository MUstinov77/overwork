from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.workspace import Workspace
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String())

    workspaces = relationship(
        "Workspace",
        uselist=True,
        back_populates="user",
        cascade="all, delete",
    )
