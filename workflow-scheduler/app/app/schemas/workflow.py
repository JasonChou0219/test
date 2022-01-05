from typing import Optional

from pydantic import BaseModel, Json


# Shared properties
class WorkflowBase(BaseModel):
    id: str
    workflow: Optional[Json] = None
    description: Optional[str] = None


# Properties to receive on workflow creation
class WorkflowCreate(WorkflowBase):
    title: str


# Properties to receive on workflow update
class WorkflowUpdate(WorkflowBase):
    pass


# Properties shared by models stored in DB
class WorkflowInDBBase(WorkflowBase):
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Workflow(WorkflowInDBBase):
    pass


# Properties stored in DB
class WorkflowInDB(WorkflowInDBBase):
    pass
