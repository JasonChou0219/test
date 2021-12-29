from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Database])
def read_databases(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve databases.
    """
    databases = crud.database.get_multi(db, skip=skip, limit=limit)
    return databases


@router.post("/", response_model=schemas.Database)
def create_database(
        *,
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
        db: Session = Depends(deps.get_db),
        id: int,
        database_in: schemas.DatabaseUpdate,
) -> Any:
    """
    Update a database.
    """
    database = crud.database.get(db=db, id=id)
    if not database:
        raise HTTPException(status_code=404, detail="Database not found")
    database = crud.database.update(db=db, db_obj=database, obj_in=database_in)
    return database


@router.get("/{id}", response_model=schemas.Database)
def read_database(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Get database by ID.
    """
    database = crud.database.get(db=db, id=id)
    if not database:
        raise HTTPException(status_code=404, detail="Database not found")
    return database


@router.delete("/{id}", response_model=schemas.Database)
def delete_database(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Delete a database.
    """
    database = crud.database.get(db=db, id=id)
    if not database:
        raise HTTPException(status_code=404, detail="Database not found")
    database = crud.database.remove(db=db, id=id)
    return database
