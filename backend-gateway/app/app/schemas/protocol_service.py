from typing import List

from pydantic import BaseModel

from .protocol_feature import ProtocolFeature


class ProtocolService(BaseModel):
    uuid: str
    features: List[ProtocolFeature]
