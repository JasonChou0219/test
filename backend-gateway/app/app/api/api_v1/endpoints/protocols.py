from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import parse_obj_as

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()
target_service_hostname = "http://sila2_manager_data-acquisition_1"  # -> to env var
target_service_port = settings.DATA_ACQUISITION_UVICORN_PORT  # -> to env var
target_service_api_version = settings.API_V1_STR  # -> to env var

target_service_url = target_service_hostname + ":" \
                     + str(settings.DATA_ACQUISITION_UVICORN_PORT) \
                     + str(settings.API_V1_STR) + "/"


@router.get("/", response_model=List[schemas.Protocol])
def read_protocols(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_user),  # get_current_active_superuser
) -> Any:
    """
    Retrieve protocols.
    """
    target_route = f"{target_service_url}protocols/"
    protocols = crud.protocol.get_multi(db, route=target_route, skip=skip, limit=limit, current_user=current_user)

    if not protocols:
        raise HTTPException(status_code=protocols.status_code,
                            detail=protocols.json()['detail'],
                            headers=protocols.headers)

    protocols = parse_obj_as(List[schemas.ProtocolInDB], protocols.json())
    return protocols


@router.post("/", response_model=schemas.Protocol)
def create_protocol(
        *,
        db: Session = Depends(deps.get_db),
        protocol_in: schemas.ProtocolCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new protocol.
    """
    target_route = f"{target_service_url}protocols/"
    protocol = crud.protocol.create_with_owner(db=db, route=target_route, obj_in=protocol_in, current_user=current_user)

    #    For future reference, if intending to simply forward the response from the service
    #    response = Response(content=protocol.content,
    #                 status_code=protocol.status_code,
    #                 headers=protocol.headers,
    #                 media_type="application/json")
    #    return response

    if not protocol:
        raise HTTPException(status_code=protocol.status_code,
                            detail=protocol.json()['detail'],
                            headers=protocol.headers)

    protocol = parse_obj_as(schemas.ProtocolInDB, protocol.json())
    return protocol


@router.put("/{id}", response_model=schemas.Protocol)
def update_protocol(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        protocol_in: schemas.ProtocolUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a protocol.
    """
    target_route = f"{target_service_url}protocols/{id}"
    protocol = crud.protocol.get(db=db, route=target_route, id=id, current_user=current_user)

    if not protocol:
        raise HTTPException(status_code=protocol.status_code,
                            detail=protocol.json()['detail'],
                            headers=protocol.headers)

    protocol = parse_obj_as(schemas.ProtocolInDB, protocol.json())
    protocol = crud.protocol.update(db=db, route=target_route, db_obj=protocol,
                                    obj_in=protocol_in, current_user=current_user)

    if not protocol:
        raise HTTPException(status_code=protocol.status_code,
                            detail=protocol.json()['detail'],
                            headers=protocol.headers)

    protocol = parse_obj_as(schemas.ProtocolInDB, protocol.json())
    return protocol


@router.get("/{id}", response_model=schemas.Protocol)
def read_protocol(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get protocol by ID.
    """
    target_route = f"{target_service_url}protocols/{id}"
    protocol = crud.protocol.get(db=db, route=target_route, id=id, current_user=current_user)

    if not protocol:
        raise HTTPException(status_code=protocol.status_code,
                            detail=protocol.json()['detail'],
                            headers=protocol.headers)

    protocol = parse_obj_as(schemas.ProtocolInDB, protocol.json())
    return protocol


@router.delete("/{id}", response_model=schemas.Protocol)
def delete_protocol(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a protocol.
    """
    target_route = f"{target_service_url}protocols/{id}"
    protocol = crud.protocol.remove(db=db, route=target_route, id=id, current_user=current_user)

    if not protocol:
        raise HTTPException(status_code=protocol.status_code,
                            detail=protocol.json()['detail'],
                            headers=protocol.headers)

    protocol = parse_obj_as(schemas.ProtocolInDB, protocol.json())
    return protocol
