from typing import Optional
from datetime import datetime
from uuid import uuid4, UUID

from pydantic import BaseModel, Json

from .workflow import WorkflowInDB


class JobStatus(IntEnum):
    WAITING_FOR_EXECUTION = 0
    SUBMITED_FOR_EXECUTION = 1
    RUNNING = 2
    FINISHED_SUCCESSFUL = 3
    FINISHED_ERROR = 4
    FINISHED_MANUALLY = 5
    UNKNOWN = 6

# Shared properties
class JobBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    workflow: WorkflowInDB = None
    workflow_type: Optiona[str] = None
    workflow_execute_at: Optional[datetime]

    # data_acquisition_protocol: Optional[Json] = None
    # data_acquisition_protocol_execute_at: Optional[datetime]

    # dataflow: Optiona[Json] = None
    # dataflow_type: Optional[str] = None
    # dataflow_execute_at: Optional[datetime]
    # database: Optional[UUID]

    # service_bookings:
    execute_at: Optional[datetime]



# Properties to receive on item creation
class JobCreate(JobBase):
    title: str
    uuid: UUID = uuid4()
    # workflow: WorkflowInDB


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
