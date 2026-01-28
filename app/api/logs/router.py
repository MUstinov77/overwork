from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.schemas.log import LogCreateUpdate, LogRetrieve

router = APIRouter(
    tags=["logs"],
)


@router.get(
    "/",
    response_model=list[LogRetrieve],
    response_model_exclude_none=True,
)
async def get_logs():
    pass


@router.get(
    "/{log_id}",
    response_model=LogRetrieve,
)
async def get_logs_by_id():
    pass


@router.post(
    "/",
    response_model=LogRetrieve,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    tags=["workspaces_logs"],
)
async def create_log(
    data: LogCreateUpdate,
):
    pass


@router.delete(
    "/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_log():
    pass


@router.patch(
    "/{log_id}",
    response_model=LogRetrieve,
)
async def update_log_by_id(updated_data: LogCreateUpdate):
    pass
