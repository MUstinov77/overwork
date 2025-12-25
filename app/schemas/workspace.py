from pydantic import BaseModel


class WorkspaceCreateUpdate(BaseModel):
    name: str

class WorkspaceRetrieve(BaseModel):
    id: int
    name: str