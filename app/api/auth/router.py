from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.auth.jwt import JWTService
from app.core.utils.encrypt import get_hashed_password
from app.models.user import User
from app.schemas.auth import Token, UserSignupLoginSchema
from app.service.user import UserService, get_user_service

BASE_PREFIX = "/auth"

router = APIRouter(
    prefix=BASE_PREFIX,
    tags=["auth"],
)


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED
)
async def signup(
        data: UserSignupLoginSchema,
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    user_data = data.model_dump()
    hashed_password = await get_hashed_password(user_data.pop("password"))
    user_data["hashed_password"] = hashed_password
    _user = await user_service.create_instance(user_data)
    return {"message": "User created"}


@router.post(
    "/login",
    response_model=Token | None
)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = await user_service.retrieve_one(User.username, form_data.username)
    if not user:
        return {"message": "Incorrect username or password"}
    token = JWTService().create_and_encode_token(user)
    return {"token": token}
