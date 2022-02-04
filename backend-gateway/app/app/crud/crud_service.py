from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.service import Service
from app.schemas.deprecated_service import ServiceCreate, ServiceUpdate


class CRUDService(CRUDBase[Service, ServiceCreate, ServiceUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ServiceCreate, owner_id: int
    ) -> Service:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Service]:
        return (
            db.query(self.model)
            .filter(Service.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


service = CRUDService(Service)
