import json
from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate
from app.api.deps import get_db_workflow_designer
from app import crud


class CRUDJob(CRUDBase[Job, JobCreate, JobUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: JobCreate, owner_id: int
    ) -> Job:
        db_designer = get_db_workflow_designer()
        _ = next(db_designer)
        flow = crud.flow.get(db=_, id=obj_in.flow_id)
        obj_in.uuid = uuid4()
        # flow like this is nice for db
        obj_in.flow = flow.flow
        obj_in.created_at = datetime.now()
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        # change flow style again for returning
        db_obj.flow = json.dumps(flow.flow)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Job]:
        return (
            db.query(self.model)
            .filter(Job.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


job = CRUDJob(Job)
