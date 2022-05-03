from pydantic import BaseModel


class Property(BaseModel):
    identifier: str
    observable: bool
    meta: bool
    interval: int
