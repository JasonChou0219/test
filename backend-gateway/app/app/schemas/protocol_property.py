from pydantic import BaseModel


class ProtocolProperty(BaseModel):
    identifier: str
    observable: bool
    meta: bool
    interval: int
