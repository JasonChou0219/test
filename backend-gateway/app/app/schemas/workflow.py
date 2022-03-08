from typing import Optional, List

from pydantic import BaseModel


# Shared properties
class WorkflowBase(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    workflow_type: Optional[str] = None
    file_name: Optional[str] = None
    services: Optional[List[str]] = None
    data: Optional[str] = None
    owner: Optional[str]
    owner_id: Optional[int]
    description: Optional[str] = None


# Properties to receive on item creation
class WorkflowCreate(WorkflowBase):
    title: str
    workflow_type: str


# Properties to receive on item update
class WorkflowUpdate(WorkflowBase):
    pass


# Properties shared by models stored in DB
class WorkflowInDBBase(WorkflowBase):
    id: str
    title: str
    workflow_type: str
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
