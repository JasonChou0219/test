from typing import Optional, List

from pydantic import BaseModel


# Shared properties
class WorkflowBase(BaseModel):
    name: Optional[str] = None
    fileName: Optional[str] = None
    services: Optional[List[str]] = None
    data: Optional[str] = None
    owner: Optional[str]
    owner_id: Optional[int]
    description: Optional[str] = None


# Properties to receive on item creation
class WorkflowCreate(WorkflowBase):
    name: str


# Properties to receive on item update
class WorkflowUpdate(WorkflowBase):
    pass


# Properties shared by models stored in DB
class WorkflowInDBBase(WorkflowBase):
    id: int
    name: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Workflow(WorkflowInDBBase):
    pass


# Properties properties stored in DB
class WorkflowInDB(WorkflowInDBBase):
    pass


# class WorkflowInDBList(BaseModel):
#     __root__: List[WorkflowInDB]
