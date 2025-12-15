from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.utils.auth import (
    ACCESS_TOKEN_EXPIRES_DAYS,
    authenticate_user,
    create_access_token
    )
from app.core.utils.encrypt import get_hashed_password
from app.db.db import session_provider
from app.models.user import User

from .schemas import Token, UserSignupLoginSchema

BASE_PREFIX = "/auth"

router = APIRouter(
    prefix=BASE_PREFIX,
    tags=["auth"],
)


@router.post(
    "/signup",
)
async def signup(
        user_data: UserSignupLoginSchema,
        session: Session = Depends(session_provider)
):
    data = user_data.model_dump()
    hashed_password = await get_hashed_password(data.pop("password"))
    user = User(**data)
    user.password = hashed_password
    session.add(user)
    return {"message": "User created"}


@router.post("/login")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Session = Depends(session_provider)
):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        return {"message": "Incorrect username or password"}
    token_timedelta = timedelta(days=ACCESS_TOKEN_EXPIRES_DAYS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=token_timedelta
    )
    return Token(access_token=access_token, token_type="bearer")
