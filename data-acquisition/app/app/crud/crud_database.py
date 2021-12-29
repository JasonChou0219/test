from app.crud.base import CRUDBase
from app.models.database import Database
from app.schemas.database import DatabaseCreate, DatabaseUpdate


class CRUDDatabase(CRUDBase[Database, DatabaseCreate, DatabaseUpdate]):
    pass


database = CRUDDatabase(Database)
