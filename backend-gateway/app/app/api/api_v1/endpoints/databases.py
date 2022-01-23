from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import parse_obj_as

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()
target_service_hostname = "http://sila2_device_manager_data-acquisition_1"  # -> to env var
target_service_port = settings.DATA_ACQUISITION_UVICORN_PORT  # -> to env var
target_service_api_version = settings.API_V1_STR  # -> to env var

target_service_url = target_service_hostname + ":" \
                     + str(settings.DATA_ACQUISITION_UVICORN_PORT) \
                     + str(settings.API_V1_STR) + "/"


@router.get("/", response_model=List[schemas.Database])
def read_databases(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_user),  # get_current_active_superuser
) -> Any:
    """
    Retrieve databases.
    """
    target_route = f"{target_service_url}databases/"
    if crud.user.is_superuser(current_user):
        databases = crud.database.get_multi(db, route=target_route, skip=skip, limit=limit, current_user=current_user)
    else:
        databases = crud.database.get_multi_by_owner(
            db=db, route=target_route, current_user=current_user, skip=skip, limit=limit
        )
    database = parse_obj_as(List[schemas.DatabaseInDB], databases.json())
    return database


@router.post("/", response_model=schemas.Database)
def create_database(
        *,
        db: Session = Depends(deps.get_db),
        database_in: schemas.DatabaseCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new database.
    """
    target_route = f"{target_service_url}databases/"
    database_in.owner = current_user.email
    database_in.owner_id = current_user.id
    database = crud.database.create_with_owner(db=db, route=target_route, obj_in=database_in, current_user=current_user)
    database = parse_obj_as(schemas.DatabaseInDB, database.json())
    return database


@router.put("/{id}", response_model=schemas.Database)
def update_database(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        database_in: schemas.DatabaseUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a database.
    """
    target_route = f"{target_service_url}databases/{id}"
    database = crud.database.get(db=db, route=target_route, id=id, current_user=current_user)
    if not database:
        raise HTTPException(status_code=404, detail="Database not found")
    else:
        database = parse_obj_as(schemas.DatabaseInDB, database.json())
        if not crud.user.is_superuser(current_user) and (database.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
    database = crud.database.update(db=db, route=target_route, db_obj=database,
                                    obj_in=database_in, current_user=current_user)
    database = parse_obj_as(schemas.DatabaseInDB, database.json())
    return database


@router.get("/{id}", response_model=schemas.Database)
def read_database(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get database by ID.
    """
    target_route = f"{target_service_url}databases/{id}"
    database = crud.database.get(db=db, route=target_route, id=id, current_user=current_user)
    if not database:
        raise HTTPException(status_code=404, detail="Database not found")
    else:
        database = parse_obj_as(schemas.DatabaseInDB, database.json())
        if not crud.user.is_superuser(current_user) and (database.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
    return database


@router.delete("/{id}", response_model=schemas.Database)
def delete_database(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a database.
    """
    target_route = f"{target_service_url}databases/{id}"
    database = crud.database.get(db=db, route=target_route, id=id, current_user=current_user)
    if not database:
        raise HTTPException(status_code=404, detail="Database not found")
    else:
        database = parse_obj_as(schemas.DatabaseInDB, database.json())
        if not crud.user.is_superuser(current_user) and (database.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")
    database = crud.database.remove(db=db, route=target_route, id=id, current_user=current_user)
    database = parse_obj_as(schemas.DatabaseInDB, database.json())
    return database


@router.get("/{id}/status", response_model=schemas.DatabaseStatus)
def read_database_status(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get database by ID.
    """
    target_route = f"{target_service_url}databases/{id}/status"
    status = crud.database.get_status(db=db, route=target_route, id=id, current_user=current_user).json()
    return status
