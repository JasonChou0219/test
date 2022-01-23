from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Request

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Database])
def read_databases(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve databases.
    """
    query_params = dict(request.query_params.items())
    for key in ['skip', 'limit']:
        query_params.pop(key)
    user = models.User(**query_params)

    if user.is_superuser:
        databases = crud.database.get_multi(db, skip=skip, limit=limit)
    else:
        databases = crud.database.get_multi_by_owner(
            db=db, owner_id=user.id, skip=skip, limit=limit
        )
    return databases


@router.post("/", response_model=schemas.Database)
def create_database(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        database_in: schemas.DatabaseCreate,
) -> Any:
    """
    Create new database.
    """
    database = crud.database.create(db=db, obj_in=database_in)
    return database


@router.put("/{id}", response_model=schemas.Database)
def update_database(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
        database_in: schemas.DatabaseUpdate,
) -> Any:
    """
    Update a database.
    """
    query_params = dict(request.query_params.items())
    for key in ['id']:
        query_params.pop(key)
    user = models.User(**query_params)

    database = crud.database.get(db=db, id=id)
    if not database:
        raise HTTPException(status_code=404, detail="Database not found")
    if not user.is_superuser and (database.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    database = crud.database.update(db=db, db_obj=database, obj_in=database_in)
    return database


@router.get("/{id}", response_model=schemas.Database)
def read_database(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Get database by ID.
    """
    query_params = dict(request.query_params.items())
    for key in ['id']:
        query_params.pop(key)
    user = models.User(**query_params)

    database = crud.database.get(db=db, id=id)
    if not database:
        raise HTTPException(status_code=404, detail="Database not found")
    if not user.is_superuser and (database.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return database


@router.delete("/{id}", response_model=schemas.Database)
def delete_database(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Delete a database.
    """
    query_params = dict(request.query_params.items())
    for key in ['id']:
        query_params.pop(key)
    user = models.User(**query_params)

    database = crud.database.get(db=db, id=id)
    if not database:
        raise HTTPException(status_code=404, detail="Database not found")
    if not user.is_superuser and (database.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    database = crud.database.remove(db=db, id=id)
    return database


@router.get("/{id}/status", response_model=schemas.DatabaseStatus)
def read_database_status(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Get database status by database ID.
    """
    database = read_database(request=request, db=db, id=id)

    return schemas.DatabaseStatus(online=True, status='some_status')
