from typing import Optional

from pydantic import BaseModel

from .protocol_service import ProtocolService


# Shared properties
class ProtocolBase(BaseModel):
    title: Optional[str] = None
    service: Optional[ProtocolService] = None
    owner: Optional[str] = None
    owner_id: Optional[int] = None


# Properties to receive on item creation
class ProtocolCreate(ProtocolBase):
    title: str
    service: ProtocolService

# Properties to receive on item update
class ProtocolUpdate(ProtocolBase):
    pass


# Properties shared by models stored in DB
class ProtocolInDBBase(ProtocolBase):
    id: int
    title: str
    service: ProtocolService
    owner: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Protocol(ProtocolInDBBase):
    pass


# Properties stored in DB
class ProtocolInDB(ProtocolInDBBase):
    pass
