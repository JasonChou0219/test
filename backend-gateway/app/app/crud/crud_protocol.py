from requests import delete, get, post, put
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base_rerouting import CRUDRerouteBase
from app.models.protocol import Protocol
from app.models.user import User
from app.schemas.protocol import ProtocolCreate, ProtocolUpdate


class CRUDProtocol(CRUDRerouteBase[Protocol, ProtocolCreate, ProtocolUpdate]):

    @staticmethod
    def create_with_owner(
            db: Session, *, route: str, obj_in: ProtocolCreate, current_user: User,
    ) -> Protocol:
        user_dict = jsonable_encoder(current_user)
        response = post(route, json=jsonable_encoder(obj_in), params=dict({}, **user_dict))
        return response

    @staticmethod
    def get_multi_by_owner(
            db: Session, *, route: str,  current_user: User, skip: int = 0, limit: int = 100
    ) -> List[Protocol]:
        user_dict = jsonable_encoder(current_user)
        response = get(route, params=dict({'skip': skip, 'limit': limit}, **user_dict))
        return response


protocol = CRUDProtocol(Protocol)
