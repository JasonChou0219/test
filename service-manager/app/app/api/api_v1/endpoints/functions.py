from typing import List, Optional, Union

from fastapi import APIRouter, Query, HTTPException
from pydantic import ValidationError
from sila2.framework import SilaConnectionError

from app import schemas
from app.schemas import FunctionResponse
from app.service_manager import client_controller

router = APIRouter()


@router.get("/connect/")
def connect_client(client_ip: str, client_port: int,  reset: str = None):
    try:
        client_controller.connect_client(client_ip, client_port, reset)
        return True
    except SilaConnectionError as connection_error:
        raise HTTPException(
            status_code=404,
            detail="SilaConnectionError: " + str(connection_error),
        )
    except ValueError as value_error:
        raise HTTPException(
            status_code=405,
            detail="ValueError: " + str(value_error),
        )


@router.get("/connect_initial/", response_model=schemas.ServiceInfo)
def connect_initial(client_ip: str, client_port: int, reset: str = None):
    try:
        service_info = client_controller.connect_initial(client_ip, client_port, reset)
        return service_info
    except SilaConnectionError as connection_error:
        raise HTTPException(
            status_code=404,
            detail="SilaConnectionError: " + str(connection_error),
        )
    except ValueError as value_error:
        raise HTTPException(
            status_code=405,
            detail="ValueError: " + str(value_error),
        )


@router.get("/discover/", response_model=List[schemas.ServiceInfo])
def mdns_discover():
    clients = client_controller.discover_clients()
    if len(clients) == 0:
        raise HTTPException(
            status_code=404,
            detail="DiscoveryError: No clients discovered",
        )
    return clients


@router.get("/browse_features/", response_model=List[schemas.Feature])
def browse_features(service_uuid: str):
    try:
        features = client_controller.browse_features(service_uuid)
    except ValidationError as validation_error:
        raise HTTPException(
            status_code=405,
            detail=str(validation_error),
        )
    except KeyError:
        raise HTTPException(
            status_code=405,
            detail=str("ClientError: No client matching " + service_uuid),
        )

    return features


@router.get("/unobservable/", response_model=schemas.FunctionResponse)
def run_function(service_uuid: str,
                 feature_identifier: str,
                 function_identifier: str,
                 is_property: bool,
                 response_identifiers: Optional[List[str]] = Query(None),
                 parameters: Optional[List[Union[int, str, float]]] = Query(None)):
    try:
        response = FunctionResponse()
        response.feature_identifier = feature_identifier
        response.function_identifier = function_identifier

        for param in parameters:
            try:
                param = float(param) if '.' in param else int(param)
            except:
                if param.lower() in ["true", "false"]:
                    param = True if param.lower() == "true" else False

        response.response = client_controller.run_function(service_uuid, feature_identifier, function_identifier, is_property,
                                                           response_identifiers=response_identifiers,
                                                           parameters=parameters)
        return response

    except ValidationError as validation_error:
        raise HTTPException(
            status_code=405,
            detail="ValidationError: " + str(validation_error),
        )
    except ValueError as value_error:
        raise HTTPException(
            status_code=405,
            detail="ClientError: " + str(value_error),
        )
    except KeyError:
        raise HTTPException(
            status_code=405,
            detail=str("ClientError: No client matching " + service_uuid),
        )
    except TypeError as type_error:
        raise HTTPException(
            status_code=405,
            detail="TypeError: " + str(type_error),
        )
    except AttributeError as attribute_error:
        if "Command" in str(attribute_error) and is_property:
            raise HTTPException(
                status_code=405,
                detail="IllegalArgument: Expected a property but identifier belong to a command",
            )
    except Exception as exception:
        raise HTTPException(
            status_code=400,
            detail=str(exception)
        )

