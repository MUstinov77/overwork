from fastapi import APIRouter, Response, status

from app.api.v1 import auth, employees, logs, workspaces

router = APIRouter()

router.include_router(auth.router)

router.include_router(workspaces.router)

router.include_router(employees.router)

router.include_router(logs.router)

@router.get("/health_check", tags=["Health Check"])
def health_check():
    return Response(content="OK", status_code=status.HTTP_200_OK)