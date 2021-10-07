from typing import List, Optional
from pydantic import BaseModel, Json


class SubInput(BaseModel):
    x: int
    y: int
    wires: Optional[List[List[str]]] = None


class SubOutput(BaseModel):
    x: int
    y: int
    wires: Optional[List[List[str]]] = None


class Node(BaseModel):
    id: str
    name: str = ""
    type: str = ""
    x: int = 0
    y: int = 0
    z: str = ""
    data: Json = None


class Flow(BaseModel):
    id: str
    disabled: bool
    info: str
    label: str
    data: Json

class Flows(BaseModel):
    pass

class SubFlow(BaseModel):
    id: str
    type: str
    name: str
    info: str
    category: str = ""
    # Not sure if pydantic conform
    #input: Optional[List[SubInput]] = None, Field(alias='in')
    #output: Optional[List[SubOutput]] = None, Field(alias='out')
    data: str = ""
