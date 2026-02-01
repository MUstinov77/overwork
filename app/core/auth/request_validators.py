from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.auth.jwt import JWTService
from app.models.user import User
from app.service.user import UserService, get_user_service

auth_schema = OAuth2PasswordBearer(tokenUrl="auth/login")


async def authenticate_user(
        token: Annotated[str, Depends(auth_schema)],
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    payload = JWTService().decode_token(token)
    user_dict = payload.get("context")
    user_id = user_dict.get("user_id")
    user = await user_service.retrieve_one(User.id, user_id)
    return user
