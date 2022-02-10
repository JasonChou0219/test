from typing import Optional

from pydantic import BaseModel, Json


# Shared properties
class WorkflowBase(BaseModel):
    uid: Optional[int] = None
    id: Optional[int] = None
    title: Optional[str] = None

    workflow_type: Optional[str] = None
    file_name: Optional[str] = None
    # services: Optional[List[str]] = None
    data: Optional[Json] = None
    owner: Optional[str]
    owner_id: Optional[int]
    description: Optional[str] = None


# Properties to receive on workflow creation
class WorkflowCreate(WorkflowBase):
    title: str
    workflow_type: str


# Properties to receive on workflow update
class WorkflowUpdate(WorkflowBase):
    pass


# Properties shared by models stored in DB
class WorkflowInDBBase(WorkflowBase):
    uid: int
    id: int
    title: str
    owner_id: int
    workflow_type: str

    class Config:
        orm_mode = True


# Properties to return to client
class Workflow(WorkflowInDBBase):
    pass


# Properties stored in DB
class WorkflowInDB(WorkflowInDBBase):
    pass
