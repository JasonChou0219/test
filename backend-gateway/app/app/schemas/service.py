from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from sila2.discovery.service_info import SilaServiceInfo


class ServiceBase(BaseModel, SilaServiceInfo):
    pass


# Properties to receive on service creation
class ServiceCreate(ServiceBase):
    pass


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
