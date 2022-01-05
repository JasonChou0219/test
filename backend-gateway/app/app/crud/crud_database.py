from requests import delete, get, post, put
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base_rerouting import CRUDRerouteBase
from app.models.database import Database
from app.models.user import User
from app.schemas.database import DatabaseCreate, DatabaseUpdate


class CRUDDatabase(CRUDRerouteBase[Database, DatabaseCreate, DatabaseUpdate]):

    @staticmethod
    def create_with_owner(
            db: Session, *, route: str, obj_in: DatabaseCreate, current_user: User,
    ) -> Database:
        user_dict = jsonable_encoder(current_user)
        response = post(route, json=jsonable_encoder(obj_in), params=dict({}, **user_dict))
        return response

    @staticmethod
    def get_multi_by_owner(
            db: Session, *, route: str,  current_user: User, skip: int = 0, limit: int = 100
    ) -> List[Database]:
        user_dict = jsonable_encoder(current_user)
        response = get(route, params=dict({'skip': skip, 'limit': limit}, **user_dict))
        return response


database = CRUDDatabase(Database)
