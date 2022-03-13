from typing import List

from pydantic import BaseModel

from .parameter import Parameter
from .response import Response


class Command(BaseModel):
    identifier: str
    observable: bool
    meta: bool
    interval: int
    parameters: List[Parameter]
    responses: List[Response]
