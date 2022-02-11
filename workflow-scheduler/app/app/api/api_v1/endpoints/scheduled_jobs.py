from requests import delete, get, post, put
from typing import Any, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.api.deps import get_db_workflow_designer_node_red

router = APIRouter()


@router.get("/", response_model=List[schemas.ScheduledJob])
def read_scheduled_jobs(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve scheduled_jobs.
    """
    query_params = dict(request.query_params.items())
    print('###############')
    print(query_params)
    for key in ['skip', 'limit']:
        query_params.pop(key)
    user = schemas.User(**query_params)

    if user.is_superuser:
        scheduled_jobs = crud.scheduled_job.get_multi(db, skip=skip, limit=limit)
    else:
        scheduled_jobs = crud.scheduled_job.get_multi_by_owner(
            db=db, owner_id=user.id, skip=skip, limit=limit
        )
    return scheduled_jobs


@router.post("/", response_model=schemas.ScheduledJob)
def create_scheduled_job(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        scheduled_job_in: schemas.ScheduledJobCreate,
) -> Any:
    """
    Create new scheduled_job.
    """
    user = schemas.User(**dict(request.query_params.items()))
    # user_dict = jsonable_encoder(user)
    # scheduled_job_in.owner_id = user.id

    try:
        scheduled_job = crud.scheduled_job.create(db=db, obj_in=scheduled_job_in)
        crud.scheduled_job.create_with_owner(db=db, obj_in=scheduled_job_in, owner_id=scheduled_job.id)
    except IntegrityError as db_exception:
        raise HTTPException(status_code=452, detail=f"{type(db_exception).__name__}:{db_exception.orig}")
    return scheduled_job


@router.put("/{id}", response_model=schemas.ScheduledJob)
def update_scheduled_job(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
        scheduled_job_in: schemas.ScheduledJobUpdate,
) -> Any:
    """
    Update a scheduled_job.
    """
    query_params = dict(request.query_params.items())
    for key in ['id']:
        query_params.pop(key)
    user = schemas.User(**query_params)

    scheduled_job = crud.scheduled_job.get(db=db, id=id)
    if not scheduled_job:
        raise HTTPException(status_code=404, detail="ScheduledJob not found")
    if not user.is_superuser and (scheduled_job.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    scheduled_job = crud.scheduled_job.update(db=db, db_obj=scheduled_job, obj_in=scheduled_job_in)
    return scheduled_job


@router.get("/{id}", response_model=schemas.ScheduledJob)
def read_scheduled_job(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Get scheduled_job by UUID.
    """
    query_params = dict(request.query_params.items())
    for key in ['id']:
        query_params.pop(key)
    user = schemas.User(**query_params)

    scheduled_job = crud.scheduled_job.get(db=db, id=id)
    if not scheduled_job:
        raise HTTPException(status_code=404, detail="ScheduledJob not found")
    if not user.is_superuser and (scheduled_job.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return scheduled_job


@router.delete("/{id}", response_model=schemas.ScheduledJob)
def delete_scheduled_job(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Delete a scheduled_job.
    """
    query_params = dict(request.query_params.items())
    for key in ['id']:
        query_params.pop(key)
    user = schemas.User(**query_params)
    scheduled_job = crud.scheduled_job.get(db=db, id=id)
    if not scheduled_job:
        raise HTTPException(status_code=404, detail="ScheduledJob not found")
    if not user.is_superuser != 'superuser' and (scheduled_job.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    scheduled_job = crud.scheduled_job.remove(db=db, id=id)
    return scheduled_job
