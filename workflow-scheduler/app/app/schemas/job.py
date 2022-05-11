from typing import Optional, Tuple, List
from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel


# Shared properties
class JobBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None
    owner_id: Optional[int] = None

    # workflow: Optional[Json] = None

    # workflow: WorkflowInDB = None
    workflows: Optional[List[Tuple[int, str, datetime]]] = []   # [workflow_id, workflow_type, workflow_execute_at]
    list_protocol_and_database: Optional[List[Tuple[int, int]]] = []   # [(protocol_id, database_id)]
    dataflow_path: Optional[str]

    # data_acquisition_protocol: Optional[Json] = None
    # data_acquisition_protocol_execute_at: Optional[datetime]
    # dataflow: Optional[Json] = None
    # dataflow_type: Optional[str] = None
    # dataflow_execute_at: Optional[datetime]
    # database: Optional[UUID]
    # service_bookings:
    execute_at: Optional[datetime] = None
    created_at: Optional[datetime] = None


# Properties to receive on item creation
class JobCreate(JobBase):
    title: str
    owner: str
    owner_id: int
    # created_at: datetime  # = datetime.now()
    # uuid: UUID = uuid4()
    # workflow: WorkflowInDB
    created_at: datetime


# Properties to receive on item update
class JobUpdate(JobBase):
    pass


# Properties shared by models stored in DB
class JobInDBBase(JobBase):
    id: int
    title: str
    owner: str
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Job(JobInDBBase):
    pass


# Properties properties stored in DB
class JobInDB(JobInDBBase):
    pass
