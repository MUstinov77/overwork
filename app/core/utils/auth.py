from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.db import session_provider
from app.models.user import User
from app.schemas.auth import TokenData

from .encrypt import verify_password
from ..exceptions import NotAuthenticatedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "0b1a876eff4cc011ca3aedec75d3096e3ddd705d0c6e2b52c806d3c135ba42fa"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRES_DAYS = 30


def get_user(
    username: str,
    session: Session
) -> User | None:
    query = select(User).where(User.username == username)
    result = session.execute(query)
    return result.scalar_one_or_none()

async def authenticate_user(
    username: str,
    password: str,
    session: Session
):
    user = get_user(username, session)
    if not user:
        return {"message": "User not found"}
    return user if await verify_password(password, user.password) else {"message": "Incorrect password"}


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Session = Depends(session_provider)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise NotAuthenticatedException
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise NotAuthenticatedException

    user = get_user(token_data.username, session)
    if not user:
        raise NotAuthenticatedException
    return user