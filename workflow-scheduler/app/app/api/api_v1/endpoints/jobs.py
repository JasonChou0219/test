from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Flow])
def read_jobs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve jobs.
    """
    if crud.user.is_superuser(current_user):
        jobs = crud.job.get_multi(db, skip=skip, limit=limit)
    else:
        jobs = crud.job.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return jobs


@router.post("/", response_model=schemas.Flow)
def create_job(
    *,
    db: Session = Depends(deps.get_db),
    job_in: schemas.JobCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    print(locals())
    """
    Create new job.
    """
    job = crud.job.create_with_owner(db=db, obj_in=job_in, owner_id=current_user.id)
    return job


@router.put("/{uuid}", response_model=schemas.Flow)
def update_job(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    job_in: schemas.JobUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a job.
    """
    job = crud.job.get(db=db, uuid=uuid)
    if not flow:
        raise HTTPException(status_code=404, detail="Job not found")
    if not crud.user.is_superuser(current_user) and (job.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    job = crud.job.update(db=db, db_obj=job, obj_in=job_in)
    return job


@router.get("/{uuid}", response_model=schemas.Flow)
def read_job(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get job by UUID.
    """
    job = crud.job.get(db=db, uuid=uuid)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not crud.user.is_superuser(current_user) and (job.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return job


@router.delete("/{uuid}", response_model=schemas.Flow)
def delete_job(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a job.
    """
    job = crud.job.get(db=db, uuid=uuid)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not crud.user.is_superuser(current_user) and (job.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    job = crud.job.remove(db=db, uuid=uuid)
    return job
