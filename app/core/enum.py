from enum import Enum


class LogType(Enum):
    sick_day = "больничный"
    vacation = "отпуск"
    day_off = "отгул"
    work_day = "работа"


class RouterType(Enum):
    workspaces = "workspaces"
    employees = "employees"