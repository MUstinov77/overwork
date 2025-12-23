from sqlalchemy import ForeignKey, Integer, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Statistics(Base):

    __tablename__ = "statistics"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    sick_days: Mapped[int] = mapped_column(
        Integer(),
        default=0
    )
    vacation: Mapped[int] = mapped_column(
        Integer(),
        default=0
    )
    vacation_surplus: Mapped[int] = mapped_column(
        Integer(),
        default=0
    )
    overwork_time: Mapped[int] = mapped_column(
        Integer(),
        default=0
    )
    days_off: Mapped[int] = mapped_column(
        Integer(),
        default=0
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey(
            "employees.id",
            ondelete="CASCADE"
        )
    )
    employee = relationship(
        "Employee",
        back_populates="statistics",
    )


@event.listens_for(Statistics, "before_insert")
def receive_before_insert(mapper, connection, target):
    if target.vacation_surplus is None:
        target.vacation_surplus = target.vacation
