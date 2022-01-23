from pydantic import BaseModel


class DatabaseStatus(BaseModel):
    online: bool
    status: str

