from typing import Optional
from uuid import UUID
from pydantic import BaseModel


# Shared properties
class ServiceBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    hostname: Optional[str] = None
    ip: Optional[str] = None
    port: Optional[int] = None
    service_uuid: Optional[UUID] = None


# Properties to receive on service creation
class ServiceCreate(ServiceBase):
    name: str
    hostname: str
    ip: str
    port: int
    service_uuid: UUID


# Properties to receive on service update
class ServiceUpdate(ServiceBase):
    pass


# Properties shared by models stored in DB
class ServiceInDBBase(ServiceBase):
    id: int
    name: str
    owner_id: int
    hostname: str
    ip: str
    port: int
    service_uuid: UUID

    class Config:
        orm_mode = True


# Properties to return to client
class Service(ServiceInDBBase):
    pass


# Properties properties stored in DB
class ServiceInDB(ServiceInDBBase):
    pass
