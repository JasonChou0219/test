from typing import List

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.job import Job
from app.models.flow import Flow
from app.schemas.job import JobCreate, JobUpdate
from app.api.deps import get_db_workflow_designer
from app.api.api_v1.endpoints import flows


class CRUDJob(CRUDBase[Job, JobCreate, JobUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: JobCreate, owner_id: int
    ) -> Job:
        flow = flows.read_flow(id= obj_in.flow_id)
        print(flow)
        obj_in.flow = flow.flow
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
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
