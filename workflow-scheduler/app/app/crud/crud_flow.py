from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.flow import Flow
from app.schemas.flow import FlowCreate, FlowUpdate
from app.api.deps import get_db_workflow_designer


class CRUDFlow(CRUDBase[Flow, FlowCreate, FlowUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: FlowCreate, owner_id: int
    ) -> Flow:
        db_designer = get_db_workflow_designer()
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Flow]:
        return (
            db.query(self.model)
            .filter(Flow.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


job = CRUDFlow(Flow)
