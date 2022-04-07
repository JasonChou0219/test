from typing import List

from pydantic import BaseModel

from .command import Command
from .property import Property


class Feature(BaseModel):
    identifier: str
    commands: List[Command]
    properties: List[Property]
