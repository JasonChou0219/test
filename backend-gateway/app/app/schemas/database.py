from typing import Optional

from pydantic import BaseModel


# Shared properties
class DatabaseBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None
    port: Optional[int] = None
    owner: Optional[str]
    owner_id: Optional[int]


# Properties to receive on item creation
class DatabaseCreate(DatabaseBase):
    title: str
    username: str
    password: str
    address: str
    port: int


# Properties to receive on item update
class DatabaseUpdate(DatabaseBase):
    pass


# Properties shared by models stored in DB
class DatabaseInDBBase(DatabaseBase):
    id: int
    title: str
    username: str
    password: str
    address: str
    port: int
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Database(DatabaseInDBBase):
    pass


# Properties stored in DB
class DatabaseInDB(DatabaseInDBBase):
    pass
