from typing import Optional, Tuple, List
from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel


class ScheduledJobStatus(IntEnum):
    WAITING_FOR_EXECUTION = 0
    SUBMITTED_FOR_EXECUTION = 1
    RUNNING = 2
    FINISHED_SUCCESSFUL = 3
    FINISHED_ERROR = 4
    FINISHED_MANUALLY = 5
    UNKNOWN = 6


# Shared properties
class ScheduledJobBase(BaseModel):
    title: str = None
    description: Optional[str] = None
    owner: str = None
    owner_id: int = None

    workflows: Optional[List[Tuple[int, str, datetime]]] = []   # [workflow_id, workflow_type, workflow_execute_at]
    list_protocol_and_database: Optional[List[Tuple[int, int]]] = []   # [(protocol_id, database_id)]
    dataflow_path: Optional[str] = None

    # data_acquisition_protocol: Optional[Json] = None
    # data_acquisition_protocol_execute_at: Optional[datetime]
    # dataflow: Optional[Json] = None
    # dataflow_type: Optional[str] = None
    # dataflow_execute_at: Optional[datetime]
    # database: Optional[UUID]
    # service_bookings:
    execute_at: datetime = None
    created_at: datetime = None
    scheduled_at: datetime = None
    job_id: Optional[int] = None
    job_status: ScheduledJobStatus = ScheduledJobStatus(6)


# Properties to receive on item creation
class ScheduledJobCreate(ScheduledJobBase):
    pass


# Properties to receive on item update
class ScheduledJobUpdate(ScheduledJobBase):
    id: int
    job_id: int
    pass


# Properties shared by models stored in DB
class ScheduledJobInDBBase(ScheduledJobBase):
    id: int
    job_id: int
    class Config:
        orm_mode = True


# Properties to return to client
class ScheduledJob(ScheduledJobInDBBase):
    pass


# Properties properties stored in DB
class ScheduledJobInDB(ScheduledJobInDBBase):
    pass
