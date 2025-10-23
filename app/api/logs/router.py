from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.utils.db_querys import get_workspace, get_employee_by_id
from app.db.models import Workspace, Employee
from .schemas import LogCreate
router = APIRouter()

@router.get(
    "/",
    response_model=list[LogCreate]
)
async def get_logs(
        workspace: Annotated[Workspace, Depends(get_workspace)],
        employee: Annotated[Employee | None, Depends(get_employee_by_id)] = None
):
    return workspace.logs if not employee else employee.logs


@router.post("/")
async def create_log(
        data: LogCreate,
        #workspace: Annotated[Workspace, Depends(get_workspace)],
        employee: Annotated[Employee, Depends(get_employee_by_id)] = None
):
    log = LogCreate(**data.model_dump())
    if not employee:
        return {"message": "cpecify employee"}
    employee.logs.append(log)
    employee.workspace.logs.append(log)
    return log
