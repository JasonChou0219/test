from pydantic import BaseModel


class ProtocolParameter(BaseModel):
    identifier: str
    value: str
