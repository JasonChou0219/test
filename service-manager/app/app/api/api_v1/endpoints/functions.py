import datetime
from typing import List, Optional, Union, Dict, Any
from uuid import UUID
from queue import Queue
from time import sleep
import json
import asyncio

from fastapi import APIRouter, Query, HTTPException, Depends, Body, WebSocket
from starlette.websockets import WebSocketDisconnect, WebSocketClose
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

from pydantic import ValidationError, parse_obj_as
from sila2.framework import SilaConnectionError
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app import schemas, crud
from app.api.deps import get_db
from app.models import ServiceInfo, Feature
from app.schemas import FunctionResponse, SilaFeatureCreate, Command
from app.schemas.sila_service_db import ServiceInfoCreate
from app.service_manager import client_controller

router = APIRouter()


@router.get("/connect/")
def connect_client(client_ip: str, client_port: int, user_id: int, user_name: str = None, reset: str = None,
                   encrypted: str = None, db: Session = Depends(get_db)):
    try:
        service_info = client_controller.connect_initial(client_ip, client_port, reset, encrypted)
        db_info = map_service_info_to_db(service_info, user_name, user_id)

        if crud.service_info.has_service_info_by_server_uuid(db, service_info.uuid) is None:
            crud.service_info.create_service_info(db=db, service_info=db_info, owner_id=user_id,
                                                  owner=user_name)

            features = client_controller.browse_features(service_info.uuid)
            converted = []
            for feature in features:
                converted.append(map_dto_to_db(feature, "").copy(exclude={'owner_uuid': True}))

            for feature in features:
                crud.feature.create_feature_for_uuid(db, map_dto_to_db(feature, service_info.uuid))
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
def connect_initial(client_ip: str, client_port: int, user_id: int, user_name: str = None, reset: str = None,
                    encrypted: str = None, db: Session = Depends(get_db)):
    try:
        service_info = client_controller.connect_initial(client_ip, client_port, reset, encrypted)
        db_info = map_service_info_to_db(service_info, user_name, user_id)

        if crud.service_info.has_service_info_by_server_uuid(db, service_info.uuid) is None:
            crud.service_info.create_service_info(db=db, service_info=db_info, owner_id=user_id,
                                                  owner=user_name)

            features = client_controller.browse_features(service_info.uuid)
            converted = []
            for feature in features:
                converted.append(map_dto_to_db(feature, "").copy(exclude={'owner_uuid': True}))

            for feature in features:
                crud.feature.create_feature_for_uuid(db=db, feature=map_dto_to_db(feature, service_info.uuid))

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


def map_service_info_to_db(service_info: schemas.ServiceInfo, user_name: str, user_id: int):
    service_info_create = ServiceInfoCreate()
    service_info_create.name = service_info.name
    service_info_create.type = service_info.type
    service_info_create.parsed_ip_address = service_info.parsed_ip_address
    service_info_create.port = service_info.port
    service_info_create.uuid = service_info.uuid
    service_info_create.version = service_info.version
    service_info_create.server_name = service_info.server_name
    service_info_create.description = service_info.description
    service_info_create.favourite = service_info.favourite
    service_info_create.isGateway = service_info.isGateway
    service_info_create.feature_names = " ".join([i for i in map(str, service_info.feature_names)])
    service_info_create.owner = user_name
    service_info_create.owner_id = user_id

    return service_info_create


def map_dto_to_db(feature: schemas.Feature, owner_uuid: str):
    feature_db = SilaFeatureCreate()
    feature_db.owner_uuid = owner_uuid
    feature_db.category = feature.category
    feature_db.feature_version = feature.feature_version
    feature_db.maturity_level = feature.maturity_level
    feature_db.originator = feature.originator
    feature_db.sila2_version = feature.sila2_version
    feature_db.identifier = feature.identifier
    feature_db.display_name = feature.display_name
    feature_db.description = feature.description
    feature_db.locale = feature.locale
    feature_db.commands = {command.identifier if hasattr(command, "identifier") else "": command for command in
                           feature.commands}
    feature_db.properties = {prop.identifier if hasattr(prop, "identifier") else "": prop for prop in
                             feature.properties}
    feature_db.errors = {err.identifier if hasattr(err, "identifier") else "": err for err in feature.errors}

    return feature_db


@router.get("/discover/", response_model=List[schemas.ServiceInfo])
def mdns_discover():
    clients = client_controller.discover_clients()
    if len(clients) == 0:
        raise HTTPException(
            status_code=404,
            detail="DiscoveryError: No clients discovered",
        )
    return clients


@router.get("/browse_clients/", response_model=List[schemas.ServiceInfo])
def browse_clients(db: Session = Depends(get_db)):
    clients = map_db_to_service_info(db)

    if len(clients) == 0:
        raise HTTPException(
            status_code=404,
            detail="DiscoveryError: No clients persisted",
        )
    return clients


@router.put("/update_service")
async def update_service(service_uuid: str, user_id: int,
                         update_data: Dict[str, Any] = Body(...),
                         super_user: str = None,
                         db: Session = Depends(get_db)):
    service_info = crud.service_info.has_service_info_by_server_uuid(db, uuid=service_uuid)

    if not service_info:
        raise HTTPException(status_code=404, detail="Item not found")
    if not super_user and (service_info.owner_id != user_id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    crud.service_info.update_service_info(db, service_uuid, update_data)
    return True


@router.get("/delete_service")
async def delete_service(service_uuid: str, user_id: int, super_user: str = None, db: Session = Depends(get_db)):
    service_info = crud.service_info.has_service_info_by_server_uuid(db, uuid=service_uuid)
    if not service_info:
        raise HTTPException(status_code=404, detail="Item not found")
    if not super_user and (service_info.owner_id != user_id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    crud.service_info.delete_service_info(db, service_uuid)
    crud.feature.remove_all_features_for_uuid(db, service_uuid)
    return True


def mapToUUID(client):
    return client.uuid


def map_db_to_service_info(db: Session):
    online_devices = client_controller.discover_clients()
    clients = []
    clients_in_db = crud.service_info.get_all_service_info(db)
    for db_client in clients_in_db:
        service_info = parse_service_info(db_client)

        if db_client.uuid in map(mapToUUID, online_devices):
            service_info.online = True
        else:
            service_info.online = False

        if db_client.uuid in client_controller.get_connected_clients():
            service_info.connected = True
            service_info.online = True
        else:
            service_info.connected = False

        clients.append(service_info)

    return list(clients)


def parse_service_info(db_client: ServiceInfo):
    service_info = schemas.ServiceInfo()
    service_info.name = db_client.name
    service_info.type = db_client.type
    service_info.parsed_ip_address = db_client.parsed_ip_address
    service_info.port = db_client.port
    service_info.uuid = db_client.uuid
    service_info.version = db_client.version
    service_info.server_name = db_client.server_name
    service_info.description = db_client.description
    service_info.favourite = db_client.favourite
    if db_client.feature_names:
        service_info.feature_names = db_client.feature_names.split()
    service_info.owner = db_client.owner
    service_info.owner_id = db_client.owner_id
    service_info.isGateway = db_client.isGateway if db_client.isGateway else False
    service_info.online = True

    return service_info


@router.get("/browse_features/", response_model=List[schemas.SilaFeatureBase])
def browse_features(service_uuid: str, db: Session = Depends(get_db)):
    try:
        features = client_controller.browse_features(service_uuid)
        converted = []
        for feature in features:
            converted.append(map_dto_to_db(feature, "").copy(exclude={'owner_uuid': True}))

    except ValidationError as validation_error:
        raise HTTPException(
            status_code=405,
            detail=str(validation_error),
        )
    except KeyError:

        db_features = crud.feature.get_all_features_for_uuid(db, service_uuid)
        if db_features:
            return db_features
        else:
            raise HTTPException(
                status_code=405,
                detail=str("ClientError: No client matching " + service_uuid),
            )

    return converted


@router.get("/disconnect")
def disconnect_client(service_uuid: str):
    try:
        client_controller.disconnect_client(service_uuid)
        return True
    except KeyError:
        raise HTTPException(
            status_code=405,
            detail=str("ClientError: No client connected matching " + service_uuid),
        )
    except Exception as exception:
        raise HTTPException(
            status_code=400,
            detail=str(exception)
        )


@router.post("/unobservable/", response_model=schemas.FunctionResponse)
def run_function(service_uuid: str,
                 feature_identifier: str,
                 function_identifier: str,
                 response_identifiers: Optional[List[str]] = Query(None),
                 parameters: Optional[List[Union[str, int, float, Any]]] = Query(None),
                 named_parameters: Optional[Dict[str, Any]] = Body(None)):
    try:
        response = FunctionResponse()
        response.feature_identifier = feature_identifier
        response.function_identifier = function_identifier

        params = []
        if parameters is not None:
            params = parameters
            for i, param in enumerate(params):
                if str(param).lower() in ["true", "false"]:
                    params[i] = True if str(param).lower() == "true" else False
                if str(param).isdecimal():  # Floats are not supported by REST query parameters
                    params[i] = int(param)
        if named_parameters is not None:
            params = named_parameters
        response.response = client_controller.run_function(service_uuid,
                                                           feature_identifier, function_identifier,
                                                           response_identifiers=response_identifiers,
                                                           parameters=params)
        for elem in response.response.values():
            elem = jsonable_encoder(elem)
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
    except Exception as exception:
        raise HTTPException(
            status_code=400,
            detail=str(exception)
        )


@router.post("/observable/", response_model=str)  # UUID
def start_observable(service_uuid: str,
                     feature_identifier: str,
                     function_identifier: str,
                     named_parameters: Optional[Dict[str, Any]] = Body(None),
                     response_identifiers: Optional[List[str]] = Query(None),
                     intermediate_identifiers: Optional[List[str]] = Query(None)) -> str:  # returns execution  UUID
    """ Registers observable in observables dict and instantiates SiLA Python client for observable """
    i = 0
    while len(list(client_controller.observables_dict.keys())) >= 100:
        execution_uuid = client_controller.observables_dict.keys()[i]
        observable_instance = client_controller.observables_dict[execution_uuid][0]
        if observable_instance.done:
            client_controller.observables_dict.pop(execution_uuid)
        elif i == 100:
            raise HTTPException(
                status_code=405,
                detail=str("ClientError: Too many active subscriptions: " + str(
                    len(list(client_controller.observables_dict.keys()))))
            )
        else:
            i += 1

    try:
        return client_controller.register_observable(
            service_uuid, feature_identifier, function_identifier, named_parameters, response_identifiers, intermediate_identifiers
        )
    except Exception as exception:
        raise HTTPException(
            status_code=400,
            detail=str(exception)
        )



class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, execution_uuid: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[execution_uuid] = websocket

    async def delete(self, execution_uuid: str):
        print(f'Delete websocket entry of {execution_uuid}. Preserve socket.')
        self.active_connections.pop(execution_uuid)

    async def disconnect_and_delete(self, execution_uuid: str):
        print(f'Disconnect and delete websocket with execution_uuid {execution_uuid}')
        await self.active_connections[execution_uuid].close()
        self.active_connections.pop(execution_uuid)

    async def disconnect(self, execution_uuid: str):
        print(f'Disconnect websocket with execution_uuid {execution_uuid}')
        await self.active_connections[execution_uuid].close()

    async def send_response(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/observable/{execution_uuid}")
async def websocket_endpoint(websocket: WebSocket, execution_uuid: str):
    if not UUID(execution_uuid) in list(client_controller.observables_dict.keys()):
        await manager.connect(execution_uuid, websocket)
        err_msg = {'status_code': 404,
                   'message': f'No observable with execution_uuid in service_manager {execution_uuid}'}
        await manager.send_response(json.dumps(err_msg, sort_keys=True, default=str), websocket)
        await manager.disconnect(execution_uuid)
        return
    else:
        await manager.connect(execution_uuid, websocket)
    print(f'A client connected to the following websocket: {execution_uuid}', flush=True)
    try:
        """ Serve websocket for observable commands """
        requested_execution_uuid = UUID(await websocket.receive_text())

        if client_controller.observables_dict[requested_execution_uuid][2]:

            if requested_execution_uuid in client_controller.observables_dict.keys():
                print('Start streaming responses')
                observable_instance = client_controller.observables_dict[requested_execution_uuid][0]
                response_queue: Queue = client_controller.observables_dict[requested_execution_uuid][1]

                while True:
                    if not response_queue.empty():
                        results = response_queue.get(timeout=1)
                        response_queue.task_done()
                        response_dict = dict(results.items())

                        result_obj = {
                            str(requested_execution_uuid): {
                                "property_response": response_dict,
                                "response": None
                            }
                        }
                        await manager.send_response(json.dumps(result_obj, sort_keys=True, default=str), websocket)
                    await asyncio.sleep(0.5)

        else:
            intermediate_response_identifiers = client_controller.observables_dict[requested_execution_uuid][3]
            response_identifiers = client_controller.observables_dict[requested_execution_uuid][4]
            execution_id_response_list = []

            if requested_execution_uuid in client_controller.observables_dict.keys():
                print('Start streaming responses')
                observable_instance = client_controller.observables_dict[requested_execution_uuid][0]
                response_queue: Queue = client_controller.observables_dict[requested_execution_uuid][1]

                while True:
                    if not response_queue.empty():
                        # Process intermediate responses
                        results = response_queue.get(timeout=1)
                        response_queue.task_done()
                        response_dict = dict(results.items())
                        responses = {}

                        for response_identifier in intermediate_response_identifiers:
                            responses.update(
                                {response_identifier: getattr(response_dict['intermediate_response'],
                                                              response_identifier)}
                            )
                        result_obj = {
                            str(requested_execution_uuid): {
                                "status": response_dict['status'].name,
                                "progress": response_dict['progress'],
                                "estimated_remaining_time": str(response_dict['estimated_remaining_time']),
                                "intermediate_response": responses,
                                "response": None
                            }
                        }
                        await manager.send_response(json.dumps(result_obj, sort_keys=True, default=str), websocket)

                    elif observable_instance.done:
                        # Send final response
                        try:
                            response = observable_instance.get_responses()
                            responses = {}
                            for response_identifier in response_identifiers:
                                responses.update(
                                    {response_identifier: getattr(response, response_identifier)}
                                )
                            result_obj = {
                                str(requested_execution_uuid): {
                                    "status": observable_instance.status.name,
                                    "progress": observable_instance.progress,
                                    "estimated_remaining_time": str(observable_instance.estimated_remaining_time),
                                    "intermediate_response": None,
                                    "response": responses
                                }
                            }
                        except Exception:
                            result_obj = {"Inside": "Empty"}
                        await manager.send_response(json.dumps(result_obj, sort_keys=True, default=str), websocket)
                        break
                    await asyncio.sleep(0.2)
    except (WebSocketDisconnect, ConnectionClosedOK, ConnectionClosedError):
        await manager.delete(execution_uuid)


@router.get("/stop_observable", status_code=204)  # UUID
def stop_observable(execution_uuid: str):  # returns execution  UUID
    """ Registers observable in observables dict and instantiates SiLA Python client for observable """
    try:
        client_controller.disconnect_websocket(execution_uuid)
        manager.disconnect_and_delete(execution_uuid)
    except KeyError:
        raise HTTPException(status_code=404,
                            detail=f"Item not found. No registered observable matching with uuid {execution_uuid}")
    return
