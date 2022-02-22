from requests import delete, get, post, put
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import BaseModel, parse_obj_as

from app.crud.base_rerouting import CRUDRerouteBase
from app.models.scheduled_job import ScheduledJob
from app.models.user import User
from app.schemas.scheduled_job import ScheduledJobCreate, ScheduledJobUpdate


class CRUDScheduledJob(CRUDRerouteBase[ScheduledJob, ScheduledJobCreate, ScheduledJobUpdate]):

    @staticmethod
    def create_with_owner(
            db: Session,
            *,
            route: str,
            obj_in: ScheduledJobCreate,
            current_user: User,
    ) -> ScheduledJob:
        user_dict = jsonable_encoder(current_user)
        response = post(route, json=jsonable_encoder(obj_in), params=dict({}, **user_dict))
        return response

    @staticmethod
    def get_multi_by_owner(
            db: Session,
            *, route: str,
            current_user: User,
            skip: int = 0,
            limit: int = 100
    ) -> List[ScheduledJob]:
        user_dict = jsonable_encoder(current_user)
        response = get(route, params=dict({'skip': skip, 'limit': limit}, **user_dict))
        return response


scheduled_job = CRUDScheduledJob(ScheduledJob)
