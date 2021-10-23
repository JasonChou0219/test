from typing import List, Dict, Optional
from dataclasses import dataclass
from pydantic import BaseModel


class Prop(BaseModel):
    p: str
    vt: str = None


class Link(BaseModel):
    id: str


class SubInput(BaseModel):
    x: int
    y: int
    wires: Optional[List[List[str]]] = None


class SubOutput(BaseModel):
    x: int
    y: int
    wires: Optional[List[List[str]]] = None


class Node(BaseModel):
    crontab: str = ""
    id: str
    name: str = ""
    once: bool = False
    onceDelay: float = 0
    payload: str = ""
    payloadType: str = ""
    repeat: str = ""
    topic: str = ""
    type: str = ""
    active: bool = False
    complete: str = ""
    console: bool = False
    statusType: str = ""
    statusVal: str = ""
    targetType: str = ""
    tosidebar: bool = False
    tostatus: bool = False
    x: int
    y: int
    z: str
    props: Optional[List[Prop]] = None
    wires: Optional[List[List[str]]] = None
    links: Optional[List[Link]] = None


class Flow(BaseModel):
    id: str
    disabled: bool
    info: str
    label: str
    type: str
    nodes: Optional[List[Node]] = None


class Subflow(BaseModel):
    id: str
    type: str
    name: str
    info: str
    category: str
    # Not sure if pydantic conform
    _in: Optional[List[SubInput]] = None
    _out: Optional[List[SubOutput]] = None
