from requests import delete, get, post, put
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, parse_obj_as
from sqlalchemy.orm import Session

from app.db.base_class import Base

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
            id: Any
    ) -> Optional[ModelType]:
        response = get(route)
        return response
        # return db.query(self.model).filter(self.model.id == id).first()

    @staticmethod
    def get_multi(
            db: Session,
            *, route: str,
            skip: int = 0,
            limit: int = 100,
            user_id: int,
    ) -> List[ModelType]:
        response = get(route, params={'skip':skip,'limit':limit, 'user_id': user_id})
        return response

    def create(self,
               *, route: str,
               obj_in: CreateSchemaType
               ) -> ModelType:
        response = post(route, json=jsonable_encoder(obj_in))
        return response

    @staticmethod
    def update(
            db: Session,
            *, route: str,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        response = put(route, json=jsonable_encoder(obj_in))
        return response

    @staticmethod
    def remove(db: Session,
               *, route: str,
               id: int,
               user_id: str) -> ModelType:
        response = delete(route, params={'id': id, 'user_id': user_id})
        return response
