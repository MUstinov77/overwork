from fastapi import FastAPI

from app.routers import workspaces

app = FastAPI()

app.include_router(workspaces.router)


@app.get("/")
async def main():
    return {"message": "Hello World"}