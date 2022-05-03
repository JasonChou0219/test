from pydantic import BaseModel


class ProtocolResponse(BaseModel):
    identifier: str
