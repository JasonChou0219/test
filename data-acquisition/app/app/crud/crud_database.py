from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.database import Database
from app.schemas.database import DatabaseCreate, DatabaseUpdate


class CRUDDatabase(CRUDBase[Database, DatabaseCreate, DatabaseUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: DatabaseCreate, owner_id: int
    ) -> Database:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Database]:
        return (
            db.query(self.model)
            .filter(Database.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


database = CRUDDatabase(Database)
