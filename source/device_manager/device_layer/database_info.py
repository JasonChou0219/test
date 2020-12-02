from dataclasses import dataclass


@dataclass
class DatabaseInfo:
    id: int
    name: str
    address: str
    port: int
    online: bool
    status: str
