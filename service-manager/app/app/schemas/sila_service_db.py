from typing import Optional

from pydantic import BaseModel


class ServiceInfoBase(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    parsed_ip_address: Optional[str] = None
    port: Optional[int] = None
    uuid: Optional[str] = None
    version: Optional[str] = None
    server_name: Optional[str] = None
    description: Optional[str] = None
    favourite: Optional[bool] = False
    feature_names: Optional[str] = None
    isGateway: Optional[bool] = None


class ServiceInfoDB(ServiceInfoBase):
    id: int

    class Config:
        orm_mode = True


class ServiceInfoCreate(ServiceInfoBase):
    owner_id: Optional[int] = 0
    owner: Optional[str] = None
    pass


# Properties to receive via API on update
class ServiceInfoUpdate(ServiceInfoBase):
    pass
