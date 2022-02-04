from requests import delete, get, post, put
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import parse_obj_as

from app import crud, models, schemas
from app.api import deps
from app.api import deps
from app.core.config import settings

router = APIRouter()
target_service_hostname = "http://sila2_device_manager_workflow-scheduler_1"  # -> to env var
target_service_port = settings.WORKFLOW_SCHEDULER_UVICORN_PORT  # -> to env var
target_service_api_version = settings.API_V1_STR  # -> to env var

target_service_url = target_service_hostname + ":" \
                     + str(settings.WORKFLOW_SCHEDULER_UVICORN_PORT) \
                     + str(settings.API_V1_STR) + "/"


@router.get("/", response_model=List[schemas.Job])
def read_jobs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),  # get_current_active_superuser
) -> Any:
    """
    Retrieve jobs.
    """
    target_route = f"{target_service_url}jobs/"
    if crud.user.is_superuser(current_user):
        jobs = crud.job.get_multi(db, route=target_route, skip=skip, limit=limit, current_user=current_user)
    else:
        jobs = crud.job.get_multi_by_owner(
            db=db, route=target_route, current_user=current_user, skip=skip, limit=limit
        )
    jobs = parse_obj_as(List[schemas.JobInDB], jobs.json())
    return jobs


@router.post("/", response_model=schemas.Job)
def create_job(
    *,
    db: Session = Depends(deps.get_db),
    job_in: schemas.JobCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new job.
    """
    target_route = f"{target_service_url}jobs/"
    job = crud.job.create_with_owner(db=db, route=target_route, obj_in=job_in, current_user=current_user)
    if not job:
        raise HTTPException(status_code=job.status_code, detail=job.json()['detail'], headers=job.headers)
    job = parse_obj_as(schemas.JobInDB, job.json())
    return job


@router.put("/{id}", response_model=schemas.Job)
def update_job(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    job_in: schemas.JobUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a job.
    """
    target_route = f"{target_service_url}jobs/{id}"
    job = crud.job.get(db=db, route=target_route, id=id, current_user=current_user)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    else:
        job = parse_obj_as(schemas.JobInDB, job.json())
        if not crud.user.is_superuser(current_user) and (job.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
    job = crud.job.update(db=db, route=target_route, db_obj=job, obj_in=job_in, current_user=current_user)
    if not job:
        raise HTTPException(status_code=job.status_code, detail=job.json()['detail'], headers=job.headers)
    job = parse_obj_as(schemas.JobInDB, job.json())
    return job


@router.get("/{id}", response_model=schemas.Job)
def read_job(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get job by ID.
    """
    target_route = f"{target_service_url}jobs/{id}"
    job = crud.job.get(db=db, route=target_route, id=id, current_user=current_user)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    else:
        job = parse_obj_as(schemas.JobInDB, job.json())
        if not crud.user.is_superuser(current_user) and (job.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
    return job


@router.delete("/{id}", response_model=schemas.Job)
def delete_job(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an job.
    """
    target_route = f"{target_service_url}jobs/{id}"
    job = crud.job.get(db=db, route=target_route, id=id, current_user=current_user)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    else:
        job = parse_obj_as(schemas.JobInDB, job.json())
        if not crud.user.is_superuser(current_user) and (job.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
        elif crud.user.is_superuser(current_user):
            # current_user.id = 'superuser'
            pass
    job = crud.job.remove(db=db, route=target_route, id=id, current_user=current_user)
    if not job:
        raise HTTPException(status_code=job.status_code, detail=job.json()['detail'], headers=job.headers)
    job = parse_obj_as(schemas.JobInDB, job.json())
    return job
