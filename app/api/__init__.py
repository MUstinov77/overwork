from fastapi import APIRouter, Response, status

from app.api.auth.router import router as auth_router
from app.api.workspaces.router import router as workspace_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(workspace_router)

@api_router.get("/health_check", tags=["Health Check"])
def health_check():
    return Response(content="OK", status_code=status.HTTP_200_OK)