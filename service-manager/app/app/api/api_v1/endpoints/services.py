from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, service_manager
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.ServiceBase])
def read_services(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve services.
    """
    if current_user == 'superuser':
        services = crud.service.get_multi(db, skip=skip, limit=limit)
    else:
        services = crud.service.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return services


@router.post("/", response_model=schemas.ServiceBase)
def create_service(
    *,
    db: Session = Depends(deps.get_db),
    service_in: schemas.ServiceCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new service.
    """

    #TODO need manual refresh?

    service = crud.service.create_with_owner(db=db, obj_in=service_in, owner_id=current_user.id)
    return service


@router.put("/{id}", response_model=schemas.ServiceBase)
def update_service(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    service_in: schemas.ServiceUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a service.
    """

    #TODO do we need HTTPExcdeptions here?
    service = crud.service.get(db=db, id=id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    if not crud.user.is_superuser(current_user) and (service.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    service = crud.service.update(db=db, db_obj=service, obj_in=service_in)
    return service


@router.get("/{id}", response_model=schemas.ServiceBase)
def read_service(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get service by ID.
    """
    service = crud.service.get(db=db, id=id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    if not crud.user.is_superuser(current_user) and (service.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return service


@router.delete("/{id}", response_model=schemas.ServiceBase)
def delete_service(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a service.
    """
    service = crud.service.get(db=db, id=id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    if not crud.user.is_superuser(current_user) and (service.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    service = crud.service.remove(db=db, id=id)
    return service


@router.get("/discovery/", response_model=List[schemas.ServiceBase])
def discover_services(
        *,
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get list of services discovered on the network.
    """
    services = service_manager.auto_discovery.find()
    if not services:
        raise HTTPException(status_code=404, detail="No services found")
    return services
