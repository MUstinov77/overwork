from pydantic import BaseModel


class WorkspaceCreateUpdateRetrieve(BaseModel):
    id: int
    name: str
