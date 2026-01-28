from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

class UserSignupLoginSchema(BaseModel):

    username: str
    password: str


class Token(BaseModel):
    token: str


class TokenData(BaseModel):
    username: str | None = None
