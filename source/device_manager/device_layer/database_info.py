from dataclasses import dataclass


@dataclass
class DatabaseInfo:
    id: int
    name: str
    address: str
    port: int

@dataclass
class DatabaseStatus:
    online: bool
    status: str
