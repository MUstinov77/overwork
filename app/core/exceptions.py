from fastapi import status
from fastapi.exceptions import HTTPException


class NotFoundException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )


class NotAuthenticatedException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )