from typing import List

from pydantic import BaseModel

from .feature import Feature


class Service(BaseModel):
    uuid: str
    features: List[Feature]
