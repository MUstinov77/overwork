from pydantic import BaseModel


class UserSignupLoginSchema(BaseModel):

    username: str
    password: str


class Token(BaseModel):
    token: str


class TokenData(BaseModel):
    username: str | None = None
