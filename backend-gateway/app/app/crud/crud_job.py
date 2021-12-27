from requests import delete, get, post, put
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import BaseModel, parse_obj_as

from app.crud.base_rerouting import CRUDRerouteBase
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate


class CRUDJob(CRUDRerouteBase[Job, JobCreate, JobUpdate]):
    def create_with_owner(
        self, db: Session, *, route: str, obj_in: JobCreate, owner_id: int
    ) -> Job:
        response = post(route, json=jsonable_encoder(obj_in))
        return response

    def get_multi_by_owner(
        self, db: Session, *, route: str,  owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Job]:
        response = get(route, params={'skip': skip, 'limit': limit, 'current_user': owner_id})
        return response

job = CRUDJob(Job)
