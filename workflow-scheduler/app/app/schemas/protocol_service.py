from typing import List

from pydantic import BaseModel

from .feature import Feature


class ProtocolService(BaseModel):
    uuid: str
    features: List[Feature]
