from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi import Request

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Job])
def read_jobs(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve jobs.
    """
    query_params = dict(request.query_params.items())
    for key in ['skip', 'limit']:
        query_params.pop(key)
    user = models.User(**query_params)

    if user.is_superuser:
        jobs = crud.job.get_multi(db, skip=skip, limit=limit)
    else:
        jobs = crud.job.get_multi_by_owner(
            db=db, owner_id=user.id, skip=skip, limit=limit
        )
    return jobs


@router.post("/", response_model=schemas.Job)
def create_job(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        job_in: schemas.JobCreate,
) -> Any:
    """
    Create new job.
    """
    user = models.User(**dict(request.query_params.items()))

    job = crud.job.create(db=db, obj_in=job_in)
    return job


@router.put("/{id}", response_model=schemas.Job)
def update_job(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
        job_in: schemas.JobUpdate,
) -> Any:
    """
    Update a job.
    """
    query_params = dict(request.query_params.items())
    for key in ['id']:
        query_params.pop(key)
    user = models.User(**query_params)

    job = crud.job.get(db=db, id=id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not user.is_superuser and (job.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    job = crud.job.update(db=db, db_obj=job, obj_in=job_in)
    return job


@router.get("/{id}", response_model=schemas.Job)
def read_job(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Get job by UUID.
    """
    query_params = dict(request.query_params.items())
    for key in ['id']:
        query_params.pop(key)
    user = models.User(**query_params)

    job = crud.job.get(db=db, id=id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not user.is_superuser and (job.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return job


@router.delete("/{id}", response_model=schemas.Job)
def delete_job(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Delete a job.
    """
    query_params = dict(request.query_params.items())
    for key in ['id']:
        query_params.pop(key)
    user = models.User(**query_params)

    job = crud.job.get(db=db, id=id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not user.is_superuser != 'superuser' and (job.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    job = crud.job.remove(db=db, id=id)
    return job
