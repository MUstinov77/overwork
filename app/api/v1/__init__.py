from fastapi import APIRouter, Response, status

from app.api.v1 import auth
from app.api.v1 import workspaces

router = APIRouter()

router.include_router(auth.router)
router.include_router(workspaces.router)

@router.get("/health_check", tags=["Health Check"])
def health_check():
    return Response(content="OK", status_code=status.HTTP_200_OK)