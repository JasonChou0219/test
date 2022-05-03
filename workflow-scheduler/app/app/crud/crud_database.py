from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.database import Database
from app.schemas.database import DatabaseCreate, DatabaseUpdate


class CRUDDatabase(CRUDBase[Database, DatabaseCreate, DatabaseUpdate]):
    def create_with_owner(
            self, db: Session, *, obj_in: DatabaseCreate, owner_id: int
    ) -> Database:
        obj_in_data = obj_in
        db_obj = self.model(**obj_in_data.json(), job_id=owner_id)
        db_obj.id = None
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Database]:
        return (
            db.query(self.model)
            .filter(Database.job_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get(self, db: Session, id: int, job_id: int) -> Database:
        return (
            db.query(self.model)
                .filter(Database.id == id,
                        Database.job_id == job_id)
                .first()
        )


class Designer(CRUDBase[Database, DatabaseCreate, DatabaseUpdate]):
    pass


database = CRUDDatabase(Database)
