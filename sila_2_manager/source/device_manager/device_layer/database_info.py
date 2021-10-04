from dataclasses import dataclass


@dataclass
class DatabaseInfo:
    id: int
    name: str
    address: str
    port: int
    username: str
    password: str

@dataclass
class DatabaseInfoNew:
    id: int
    name: str
    address: str
    port: int
    username: str
    password: str


@dataclass
class DatabaseStatus:
    online: bool
    status: str

# Todo: Use the new DatabaseStatus class
@dataclass
class DatabaseStatusNew:
    online: bool
    retention_policy: str
    error: str
    ping: float
    version: str
