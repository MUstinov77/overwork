from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models.base import Base

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
