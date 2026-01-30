from fastapi.middleware import Middleware
from fastapi import Request
from starlette.middleware.base import RequestResponseEndpoint


class AuthMiddleware(Middleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            print("No auth header")
        response = await call_next(request)
