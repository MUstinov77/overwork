from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select

from app.db.db import session_provider
from app.db.models import User


router = APIRouter(
    prefix="/users"
)

@router.get("/{user_id}")
async def get_me(
        user_id: int,
        session: Depends(session_provider)
):
    query = select(User).where(User.id == user_id)
    result = session.execute(query)
    if not result:
        return {"message": "User not found"}
    return result.one_or_none()

