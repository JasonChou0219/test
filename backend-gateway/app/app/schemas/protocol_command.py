from typing import List

from pydantic import BaseModel

from .protocol_parameter import ProtocolParameter
from .protocol_response import ProtocolResponse


class ProtocolCommand(BaseModel):
    identifier: str
    observable: bool
    meta: bool
    interval: int
    parameters: List[ProtocolParameter]
    responses: List[ProtocolResponse]
