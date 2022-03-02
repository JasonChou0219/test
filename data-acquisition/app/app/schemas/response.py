from pydantic import BaseModel


class Response(BaseModel):
    identifier: str
