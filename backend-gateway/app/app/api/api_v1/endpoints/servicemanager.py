from fastapi import APIRouter, Depends, HTTPException
from typing import Any, List

from pydantic import parse_obj_as
from requests import Session

from app import schemas, crud, models
from app.api import deps
from app.core.config import settings

router = APIRouter()
target_service_hostname = "http://sila2_device_manager_service-manager"  # -> to env var
target_service_port = settings.SERVICE_MANAGER_UVICORN_PORT  # -> to env var
target_service_api_version = settings.API_V1_STR  # -> to env var

target_service_url = target_service_hostname + ":" \
                     + str(settings.SERVICE_MANAGER_UVICORN_PORT) \
                     + str(settings.API_V1_STR) + "/"

target_route = f"{target_service_url}servicemanager/"


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

    if crud.user.is_superuser(current_user):
        services = crud.service.get_multi(db, route=target_route, skip=skip, limit=limit, current_user='superuser')
    else:
        services = crud.service.get_multi_by_owner(
            db=db, route=target_route, owner_id=current_user.id, skip=skip, limit=limit
        )
        services = parse_obj_as(List[schemas.ServiceInDB], services.json())

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
    service_in.owner = current_user.email
    service_in.owner_id = current_user.id
    service = crud.service.create_with_owner(db=db, route=target_route, obj_in=service_in, owner_id=current_user.id)
    service = parse_obj_as(schemas.ServiceInDB, service.json())

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
    update_target = target_route + f"/{id}"

    service = crud.service.get(db=db, route=update_target, id=id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    if not crud.user.is_superuser(current_user) and (service.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    service = crud.service.update(db=db, route=target_route, db_obj=service, obj_in=service_in)
    service = parse_obj_as(schemas.ServiceInDB, service.json())

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
    update_target = target_route + f"/{id}"
    service = crud.service.get(db=db, route=update_target, id=id)

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    else:
        service = parse_obj_as(schemas.ServiceInDB, service.json())
        if not crud.user.is_superuser(current_user) and (service.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")

    service = parse_obj_as(schemas.ServiceInDB, service.json())
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
    update_target = target_route + f"/{id}"

    service = crud.service.get(db=db, route=update_target, id=id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    else:
        service = parse_obj_as(schemas.ServiceInDB, service.json())
        if not crud.user.is_superuser(current_user) and (service.owner_id != current_user.id):
            raise HTTPException(status_code=400, detail="Not enough permissions")

    service = crud.service.remove(db=db, route=target_route, id=id, current_user=current_user.id)
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
