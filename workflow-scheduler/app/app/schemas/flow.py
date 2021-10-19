from typing import Optional

from pydantic import BaseModel


# Shared properties
class FlowBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class FlowCreate(FlowBase):
    title: str


# Properties to receive on item update
class FlowUpdate(FlowBase):
    pass


# Properties shared by models stored in DB
class FlowInDBBase(FlowBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Item(FlowInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(FlowInDBBase):
    pass
