from typing import Optional, Dict, Union, List, Final
from uuid import UUID
from pydantic import BaseModel
from sila2.discovery.service_info import SilaServiceInfo

_DNS_HOST_TTL: Final = 120  # two minute for host records (A, SRV etc) as-per RFC6762, protected in zeroconfig
_DNS_OTHER_TTL: Final = 4500  # 75 minutes for non-host records (PTR, TXT etc) as-per RFC6762, protected in zeroconfig


# Shared properties
class ServiceBase(BaseModel, SilaServiceInfo):
    isEdge: bool
    pass


# Properties to receive on service creation
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
