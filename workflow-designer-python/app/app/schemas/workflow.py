from typing import Optional, List

from pydantic import BaseModel


# Shared properties
class WorkflowBase(BaseModel):
    title: Optional[str] = None
    workflow_type: Optional[str] = None
    file_name: Optional[str] = None
    # services: Optional[List[str]] = None
    data: Optional[str] = None
    owner: str
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
    id: int
    title: str
    owner_id: int
    workflow_type: str

    class Config:
        orm_mode = True

# Properties to return to client
class Workflow(WorkflowInDBBase):
    pass


# Properties properties stored in DB
class WorkflowInDB(WorkflowInDBBase):
    pass
