from typing import Optional, List
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Json


# Shared properties
class JobBase(BaseModel):
    flow: Optional[Json] = None
    execute_at: Optional[datetime]
    description: Optional[str] = None


# Properties to receive on item creation
class JobCreate(JobBase):
    title: str
    flow_id: str
    uuid: Optional[UUID]


# Properties to receive on item update
class JobUpdate(JobBase):
    pass


# Properties shared by models stored in DB
class JobInDBBase(JobBase):
    uuid: UUID
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Job(JobInDBBase):
    pass


# Properties properties stored in DB
class JobInDB(JobInDBBase):
    pass
