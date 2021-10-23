from typing import Optional
from datetime import datetime
from uuid import uuid4, UUID

from pydantic import BaseModel, Json



# Shared properties
class JobBase(BaseModel):
    flow: Optional[Json] = None
    execute_at: Optional[datetime]
    description: Optional[str] = None


# Properties to receive on item creation
class JobCreate(JobBase):
    title: str
    uuid: UUID = uuid4()



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
