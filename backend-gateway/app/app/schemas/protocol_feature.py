from typing import List

from pydantic import BaseModel

from .protocol_command import ProtocolCommand
from .protocol_property import ProtocolProperty


class ProtocolFeature(BaseModel):
    identifier: str
    commands: List[ProtocolCommand]
    properties: List[ProtocolProperty]
