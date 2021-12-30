from requests import delete, get, post, put
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base_rerouting import CRUDRerouteBase
from app.models.workflow import Workflow
from app.models.user import User
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate


class CRUDWorkflow(CRUDRerouteBase[Workflow, WorkflowCreate, WorkflowUpdate]):
    def create_with_owner(
        self, db: Session, *, route: str, obj_in: WorkflowCreate, current_user: User,
    ) -> Workflow:
        user_dict = jsonable_encoder(current_user)
        response = post(route, json=jsonable_encoder(obj_in), params=dict({}, **user_dict))
        return response

    def get_multi_by_owner(
        self, db: Session, *, route: str,  current_user: User, skip: int = 0, limit: int = 100
    ) -> List[Workflow]:
        user_dict = jsonable_encoder(current_user)
        response = get(route, params=dict({'skip': skip, 'limit': limit}, **user_dict))
        return response

workflow = CRUDWorkflow(Workflow)
