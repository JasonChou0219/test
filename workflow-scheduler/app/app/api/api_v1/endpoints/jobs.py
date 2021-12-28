from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Job])
def read_jobs(
    user_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve jobs.
    """
    # if crud.user.is_superuser(current_user):
    print('HERE')
    print(user_id, skip, limit)
    print('THERE')
    if user_id == 'superuser':
        jobs = crud.job.get_multi(db, skip=skip, limit=limit)
    else:
        jobs = crud.job.get_multi_by_owner(
            db=db, owner_id=user_id, skip=skip, limit=limit
        )
    return jobs


@router.post("/", response_model=schemas.Job)
def create_job(
    *,
    db: Session = Depends(deps.get_db),
    job_in: schemas.JobCreate,
) -> Any:
    """
    Create new job.
    """
    print('HERE')
    print(job_in)
    print('THERE')
    model = models.Job
    obj_in_data = jsonable_encoder(job_in)
    job = model(**obj_in_data)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.put("/{id}", response_model=schemas.Job)
def update_job(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    job_in: schemas.JobUpdate,
) -> Any:
    """
    Update a job.
    """
    job = crud.job.get(db=db, id=id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    # if not crud.user.is_superuser(current_user) and (job.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    job = crud.job.update(db=db, db_obj=job, obj_in=job_in)
    return job


@router.get("/{id}", response_model=schemas.Job)
def read_job(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get job by UUID.
    """
    job = crud.job.get(db=db, id=id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    # if not crud.user.is_superuser(current_user) and (job.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    return job


@router.delete("/{id}", response_model=schemas.Job)
def delete_job(
    user_id: int,
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete a job.
    """
    job = crud.job.get(db=db, id=id)
    print('Got to delete')
    print(job)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    # if current_user != 'superuser' and (job.owner_id != current_user):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    job = crud.job.remove(db=db, id=id)
    return job
