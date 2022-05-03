from pydantic import BaseModel


class Parameter(BaseModel):
    identifier: str
    value: str
