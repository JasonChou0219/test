from requests import delete, get, post, put
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base
from app.models.user import User

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDRerouteBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    @staticmethod
    def get(
            db: Session,
            route: str,
            id: int,
            current_user: User,
    ) -> Optional[ModelType]:
        user_dict = jsonable_encoder(current_user)
        response = get(route, params=dict({'id': id}, **user_dict))
        return response
        # return db.query(self.model).filter(self.model.id == id).first()

    @staticmethod
    def get_multi(
            db: Session,
            *, route: str,
            skip: int = 0,
            limit: int = 100,
            current_user: User,
    ) -> List[ModelType]:
        user_dict = jsonable_encoder(current_user)
        response = get(route, params=dict({'skip': skip, 'limit': limit}, **user_dict))
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
