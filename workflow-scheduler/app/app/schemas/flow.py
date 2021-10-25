from typing import Optional, List

from pydantic import BaseModel, Json


# Shared properties
class FlowBase(BaseModel):
    id: str
    flow: Optional[List[Json]] = None
    description: Optional[str] = None


# Properties to receive on item creation
class FlowCreate(FlowBase):
    title: str


# Properties to receive on item update
class FlowUpdate(FlowBase):
    pass


# Properties shared by models stored in DB
class FlowInDBBase(FlowBase):
    title: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Flow(FlowInDBBase):
    pass


# Properties properties stored in DB
class FlowInDB(FlowInDBBase):
    pass
