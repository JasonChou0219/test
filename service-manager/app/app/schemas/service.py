from uuid import UUID
from pydantic import BaseModel
from sila2.client import SilaClient


# Shared properties
class ServiceBase(BaseModel, SilaClient):
    pass


# Properties to receive on service creatio
class ServiceCreate(ServiceBase):
    owner: str
    owner_id: str
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
