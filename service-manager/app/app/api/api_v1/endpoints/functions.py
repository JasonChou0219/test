from typing import List, Optional

from fastapi import APIRouter, Query

from app import schemas
from app.schemas import FunctionResponse
from app.service_manager import client_controller

router = APIRouter()


@router.get("/connect", response_model=List[schemas.Feature])
def connect_client(client_ip: str, client_port: int):
    return client_controller.connect_client(client_ip, client_port)


@router.get("/function", response_model=schemas.FunctionResponse)
def run_function(client_ip: str,
                 client_port: int,
                 identifier: str,
                 function: str,
                 is_property: bool,
                 is_observable: bool,
                 response_identifiers: Optional[List[str]] = Query(None),
                 parameters: Optional[List[str]] = Query(None)):
    response = FunctionResponse()
    response.feature_identifier = identifier
    response.function_identifier = function

    response.response = client_controller.run_function(client_ip, client_port, identifier, function, is_property,
                                                       is_observable, response_identifiers=response_identifiers,
                                                       parameters=parameters)

    return response
