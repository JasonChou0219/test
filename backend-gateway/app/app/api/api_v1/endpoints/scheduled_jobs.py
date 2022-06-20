from requests import delete, get, post, put
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import parse_obj_as

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()
target_service_hostname = "http://sila2_manager_workflow-scheduler_1"  # -> to env var
target_service_port = settings.WORKFLOW_SCHEDULER_UVICORN_PORT  # -> to env var
target_service_api_version = settings.API_V1_STR  # -> to env var

target_service_url = target_service_hostname + ":" \
                     + str(settings.WORKFLOW_SCHEDULER_UVICORN_PORT) \
                     + str(settings.API_V1_STR) + "/"


@router.get("/", response_model=List[schemas.ScheduledJob])
def read_scheduled_jobs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),  # get_current_active_superuser
) -> Any:
    """
    Retrieve scheduled_jobs.
    """
    target_route = f"{target_service_url}scheduled_jobs/"
    if crud.user.is_superuser(current_user):
        scheduled_jobs = crud.scheduled_job.get_multi(
            db, route=target_route, skip=skip, limit=limit, current_user=current_user)
    else:
        scheduled_jobs = crud.scheduled_job.get_multi_by_owner(
            db=db, route=target_route, current_user=current_user, skip=skip, limit=limit
        )
    scheduled_jobs = parse_obj_as(List[schemas.ScheduledJobInDB], scheduled_jobs.json())
    return scheduled_jobs


@router.post("/", response_model=schemas.ScheduledJob)
def create_scheduled_job(
    *,
    db: Session = Depends(deps.get_db),
    scheduled_job_in: schemas.ScheduledJobCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new scheduled_job.
    """
    target_route = f"{target_service_url}scheduled_jobs/"
    scheduled_job = crud.scheduled_job.create_with_owner(
        db=db, route=target_route, obj_in=scheduled_job_in, current_user=current_user)
    if not scheduled_job:
        raise HTTPException(
            status_code=scheduled_job.status_code, detail=scheduled_job.json()['detail'], headers=scheduled_job.headers)
    scheduled_job = parse_obj_as(schemas.ScheduledJobInDB, scheduled_job.json())
    return scheduled_job


@router.put("/{id}", response_model=schemas.ScheduledJob)
def update_scheduled_job(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    scheduled_job_in: schemas.ScheduledJobUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a scheduled_job.
    """
    target_route = f"{target_service_url}scheduled_jobs/{id}"
    scheduled_job = crud.scheduled_job.get(db=db, route=target_route, id=id, current_user=current_user)
    if not scheduled_job:
        raise HTTPException(status_code=404, detail="ScheduledJob not found")
    else:
        scheduled_job = parse_obj_as(schemas.ScheduledJobInDB, scheduled_job.json())
        if not crud.user.is_superuser(current_user) and (scheduled_job.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
    scheduled_job = crud.scheduled_job.update(
        db=db, route=target_route, db_obj=scheduled_job, obj_in=scheduled_job_in, current_user=current_user)
    if not scheduled_job:
        raise HTTPException(
            status_code=scheduled_job.status_code, detail=scheduled_job.json()['detail'], headers=scheduled_job.headers)
    scheduled_job = parse_obj_as(schemas.ScheduledJobInDB, scheduled_job.json())
    return scheduled_job


@router.get("/{id}", response_model=schemas.ScheduledJob)
def read_scheduled_job(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get scheduled_job by ID.
    """
    target_route = f"{target_service_url}scheduled_jobs/{id}"
    scheduled_job = crud.scheduled_job.get(db=db, route=target_route, id=id, current_user=current_user)
    if not scheduled_job:
        raise HTTPException(status_code=404, detail="ScheduledJob not found")
    else:
        scheduled_job = parse_obj_as(schemas.ScheduledJobInDB, scheduled_job.json())
        if not crud.user.is_superuser(current_user) and (scheduled_job.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
    return scheduled_job


@router.delete("/{id}", response_model=schemas.ScheduledJob)
def delete_scheduled_job(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a scheduled_job.
    """
    target_route = f"{target_service_url}scheduled_jobs/{id}"
    scheduled_job = crud.scheduled_job.get(db=db, route=target_route, id=id, current_user=current_user)
    if not scheduled_job:
        raise HTTPException(status_code=404, detail="ScheduledJob not found")
    else:
        scheduled_job = parse_obj_as(schemas.ScheduledJobInDB, scheduled_job.json())
        if not crud.user.is_superuser(current_user) and (scheduled_job.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
        elif crud.user.is_superuser(current_user):
            # current_user.id = 'superuser'
            pass
    scheduled_job = crud.scheduled_job.remove(db=db, route=target_route, id=id, current_user=current_user)
    if not scheduled_job:
        raise HTTPException(
            status_code=scheduled_job.status_code,
            detail=scheduled_job.json()['detail'],
            headers=scheduled_job.headers)
    scheduled_job = parse_obj_as(schemas.ScheduledJobInDB, scheduled_job.json())
    return scheduled_job
