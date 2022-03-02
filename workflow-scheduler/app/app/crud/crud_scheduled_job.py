from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.scheduled_job import ScheduledJob
from app.schemas.scheduled_job import ScheduledJobCreate, ScheduledJobUpdate


class CRUDScheduledJob(CRUDBase[ScheduledJob, ScheduledJobCreate, ScheduledJobUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ScheduledJobCreate, owner_id: int
    ) -> ScheduledJob:
        obj_in.owner_id = owner_id
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[ScheduledJob]:
        return (
            db.query(self.model)
            .filter(ScheduledJob.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


scheduled_job = CRUDScheduledJob(ScheduledJob)
