from requests import delete, get, post, put
# Todo: Delete once API call is running
from requests import Response
from typing import List, Type

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import parse_obj_as

from app.crud.base_rerouting import CRUDRerouteBase
from app.models.workflow import Workflow
from app.models.user import User
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate, WorkflowInDB, WorkflowBase

from app.api.deps import get_db_workflow_designer_node_red


class CRUDWorkflow(CRUDRerouteBase[Workflow, WorkflowCreate, WorkflowUpdate]):

    @staticmethod
    def create_with_owner(
        db: Session, *, route: str, obj_in: WorkflowCreate, current_user: User,
    ) -> Workflow:
        user_dict = jsonable_encoder(current_user)
        response = post(route, json=jsonable_encoder(obj_in), params=dict({}, **user_dict))
        return response

    @staticmethod
    def get_multi_by_owner(
        db: Session, *, route: str,  current_user: User, skip: int = 0, limit: int = 100
    ) -> List[Workflow]:
        # Get the python workflows
        user_dict = jsonable_encoder(current_user)
        response_python = get(route, params=dict({'skip': skip, 'limit': limit}, **user_dict))
        print(response_python)

        # Get the node red workflows
        db_node_red_designer = next(get_db_workflow_designer_node_red())
        #response_node_red = db_node_red_designer.query(List[Workflow]).offset(skip).limit(limit).all()
        #print(response_node_red)

        # Todo: Concatenate responses
        response = response_python  # + response_node_red
        return response

    @staticmethod
    def get_multi(db: Session, *, route: str, wf_type: str = "python", skip: int = 0, limit: int = 100, current_user: User) -> List[Workflow]:
        user_dict = jsonable_encoder(current_user)
        response = []
        if wf_type == "python":
            # print('+++++++Py+++++++')
            response = get(route, params=dict({'skip': skip, 'limit': limit}, **user_dict))
            response = parse_obj_as(List[WorkflowInDB], response.json())
        elif wf_type == "node-red":
            # print('+++++++NR+++++++')
            response = get(route)
            response = response.json()
            for workflowItem in response:
                workflowItem["owner_id"] = current_user.id
        return response

    """
    @staticmethod
    def get(db: Session, route: str, id: int, current_user: User) -> Workflow:
        user_dict = jsonable_encoder(current_user)
        # response = get(route, params=dict({'id': id}, **user_dict))
        response = get(route, params=dict(**user_dict))
        return response
        # return db.query(self.model).filter(self.model.id == id).first()

    @staticmethod
    def get_multi(db: Session,*, route: str, skip: int = 0,limit: int = 100,current_user: User) -> List[ModelType]:
        user_dict = jsonable_encoder(current_user)
        response = get(route, params=dict({'skip': skip, 'limit': limit}, **user_dict))
        
        user_dict = jsonable_encoder(current_user)
        response_python = get(route, params=dict({'skip': skip, 'limit': limit}, **user_dict))
        print(response_python)

        # Get the node red workflows
        db_node_red_designer = next(get_db_workflow_designer_node_red())
        response_node_red = db_node_red_designer.query(List[Workflow]).offset(skip).limit(limit).all()
        print(response_node_red)

        # Todo: Concatenate responses
        response = response_python  # + response_node_red
        
        return response

    @staticmethod
    def create(
            *, route: str,
            obj_in: CreateSchemaType,
            current_user: User,
    ) -> ModelType:
        user_dict = jsonable_encoder(current_user)
        response = post(route, json=jsonable_encoder(obj_in), params=dict({}, **user_dict))
        return response

    @staticmethod
    def update(
            db: Session,
            *, route: str,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]],
            current_user: User,
    ) -> ModelType:
        user_dict = jsonable_encoder(current_user)
        response = put(route, json=jsonable_encoder(obj_in), params=dict({}, **user_dict))
        return response

    @staticmethod
    def remove(db: Session,
               *, route: str,
               id: int,
               current_user: User,
               ) -> ModelType:
        user_dict = jsonable_encoder(current_user)
        response = delete(route, params=dict({'id': id}, **user_dict))
        return response
    """

workflow = CRUDWorkflow(Workflow)
