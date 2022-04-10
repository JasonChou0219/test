from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Request
from requests.exceptions import ConnectionError
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError

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
    check_database_details(database_in)

    query_params = dict(request.query_params.items())
    user = models.User(**query_params)

    database_in.owner_id = user.id
    database_in.owner = user.email

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
    user = models.User(**query_params)

    database = crud.database.get(db=db, id=id)
    if not database:
        raise HTTPException(status_code=404, detail="Database not found")
    if not user.is_superuser and (database.owner_id != user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    check_database_details(database_in)

    database_in.owner_id = user.id
    database_in.owner = user.email

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

    client = InfluxDBClient(host=database.address, port=database.port, username=database.username,
                            password=database.password, database=database.name, timeout=0.5)
    try:
        # Attempt to create a database, which checks both that the connection details are correct
        # and that the user has admin privileges
        client.create_database(database.name)
        # Attempt to create a retention policy, which checks that the specified retention policy is valid
        client.create_retention_policy(name=database.retention_policy,
                                       duration=database.retention_policy,
                                       replication='1',
                                       database=database.name)
    # Timeout, meaning the database cannot be reached
    except ConnectionError:
        return schemas.DatabaseStatus(online=False, status='Database not found for connection details')
    # User must be admin
    except InfluxDBClientError as e:
        # User must be admin
        if e.code == 401 or e.code == 403:
            return schemas.DatabaseStatus(online=False, status='Not enough permissions')
        # Retention policy must be valid
        elif e.code == 400:
            return schemas.DatabaseStatus(online=False, status='Invalid retention policy')
        else:
            return schemas.DatabaseStatus(online=False, status=e.content)

    return schemas.DatabaseStatus(online=True, status='Ready')


def check_database_details(database: schemas.Database) -> None:
    client = InfluxDBClient(host=database.address, port=database.port, username=database.username,
                            password=database.password, database=database.name, timeout=0.5)
    try:
        # Attempt to create a database, which checks both that the connection details are correct
        # and that the user has admin privileges
        client.create_database(database.name)
        # Check if the specified retention policy exists
        client.switch_database(database.name)
        retention_policies = client.get_list_retention_policies()
        retention_policy_exists = False
        for retention_policy in retention_policies:
            if retention_policy['name'] == database.retention_policy:
                retention_policy_exists = True
        # If retention policy does not exist, attempt to create a new one
        if not retention_policy_exists:
            client.create_retention_policy(name=database.retention_policy,
                                           duration=database.retention_policy,
                                           replication='1',
                                           database=database.name)
    # Timeout, meaning the database cannot be reached
    except ConnectionError:
        raise HTTPException(status_code=404, detail="Database not found for connection details")
    except InfluxDBClientError as e:
        # User must be admin
        if e.code == 401 or e.code == 403:
            raise HTTPException(status_code=401, detail="Not enough permissions")
        # Retention policy must be valid
        elif e.code == 400:
            raise HTTPException(status_code=400, detail="Invalid retention policy")
        else:
            raise HTTPException(status_code=e.code, detail=e.content)
