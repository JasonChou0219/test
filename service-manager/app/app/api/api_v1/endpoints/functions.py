from typing import List, Optional

from fastapi import APIRouter, Query

from app import schemas
from app.schemas import FunctionResponse
from app.service_manager import client_controller

router = APIRouter()


@router.get("/connect/")
def connect_client(client_ip: str, client_port: int):
    client_controller.connect_client(client_ip, client_port)
    return True


@router.get("/discover/", response_model=List[schemas.ServiceInfo])
def mdns_discover():
    return client_controller.discover_clients()


@router.get("/browse_features/", response_model=List[schemas.Feature])
def browse_features(service_uuid: str):
    return client_controller.browse_features(service_uuid)


@router.get("/unobservable/", response_model=schemas.FunctionResponse)
def run_function(service_uuid: str,
                 identifier: str,
                 function: str,
                 is_property: bool,
                 is_observable: bool,
                 response_identifiers: Optional[List[str]] = Query(None),
                 parameters: Optional[List[str]] = Query(None)):
    response = FunctionResponse()
    response.feature_identifier = identifier
    response.function_identifier = function

    response.response = client_controller.run_function(service_uuid, identifier, function, is_property,
                                                       is_observable, response_identifiers=response_identifiers,
                                                       parameters=parameters)

    return response
