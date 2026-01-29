from typing import Annotated

from fastapi import Depends, Request, Response

from app.service.user import UserService, get_user_service


def get_auth_dependency():
    return Depends(validate_auth)


async def validate_auth(
        request: Request,
        response: Response,
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    authorization = request.headers.get("Authorization")
    if not authorization:
        print("Authorization header not found")
    print("Authorization header found")



AuthenticatedUser = Annotated[dict, get_auth_dependency()]