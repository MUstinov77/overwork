from fastapi.exceptions import HTTPException
from pwdlib import PasswordHash

from app.models.user import User


def get_auth_service():
    return AuthService()

class AuthService:

    hash_checker = PasswordHash.recommended()

    def verify_password(self, plain_password, hashed_password):
        return self.hash_checker.verify(plain_password, hashed_password)

    async def get_password_hash(self, password):
        return self.hash_checker.hash(password)

    async def login(self, user: User, password):
        if not self.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=400,
                detail="Incorrect username or password",
            )
        return {
            "user_id": user.id,
            "username": user.username
        }

