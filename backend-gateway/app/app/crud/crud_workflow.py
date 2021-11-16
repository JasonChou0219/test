from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import BaseModel, parse_obj_as

from app.crud.base_rerouting import CRUDRerouteBase
from app.models.workflow import Workflow
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate


class CRUDWorkflow(CRUDRerouteBase[Workflow, WorkflowCreate, WorkflowUpdate]):
    def create_with_owner(
        self, db: Session, *, route: str, obj_in: WorkflowCreate, owner_id: int
    ) -> Workflow:
        # Todo: Implement rerouting
        print(route)
        print(obj_in)
        print(owner_id)
        # response = get(route)
        # obj_in_data = jsonable_encoder(obj_in)
        # db_obj = self.model(**obj_in_data, owner_id=owner_id)
        # db.add(db_obj)
        # db.commit()
        # db.refresh(db_obj)
        # return db_obj

    def get_multi_by_owner(
        self, db: Session, *, route: str,  owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Workflow]:
        # Todo: Implement rerouting
        print(route)
        return (
            db.query(self.model)
            .filter(Workflow.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


workflow = CRUDWorkflow(Workflow)
