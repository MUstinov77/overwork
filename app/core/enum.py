from enum import Enum


class LogType(Enum):
    sick_days = "больничный"
    vacation = "отпуск"
    days_off = "отгул"


class RouterType(Enum):
    workspaces = "workspaces"
    employees = "employees"