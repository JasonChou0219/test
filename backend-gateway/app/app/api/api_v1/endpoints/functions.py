import json
from typing import List, Optional, Union, Any, Dict
from uuid import UUID
import aiohttp
from aiohttp import ClientConnectorError
from fastapi import APIRouter, Query, HTTPException, Depends, Body, WebSocket
from starlette.websockets import WebSocketDisconnect, WebSocketClose
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
import websockets

from app import schemas, models
from app.api import deps
from app.core.config import settings
from app.websocket_control import websocket_buffer

router = APIRouter()
target_service_hostname = "http://sila2_manager_service-manager_1"  # -> to env var
target_service_hostname_ws = "ws://sila2_manager_service-manager_1"  # -> to env var
target_service_port = settings.SERVICE_MANAGER_UVICORN_PORT  # -> to env var
target_service_api_version = settings.API_V1_STR  # -> to env var

target_service_url = target_service_hostname + ":" \
                     + str(settings.SERVICE_MANAGER_UVICORN_PORT) \
                     + str(settings.API_V1_STR) + "/"
target_service_ws_url = target_service_hostname_ws + ":" \
                        + str(settings.SERVICE_MANAGER_UVICORN_PORT) \
                        + str(settings.API_V1_STR) + "/"


@router.get("/connect")
async def connect_to_client(client_ip: str, client_port: int, reset: bool = False, encrypted: bool = False,
                            # current_user: models.User = Depends(deps.get_current_active_user)
                            ):
    target_route = target_service_url + "sm_functions/connect/"
    query_params = [('client_ip', client_ip), ('client_port', client_port),
                    ('user_id', 0)]
    # if current_user.full_name:
    # query_params.append(('user_name', current_user.full_name))
    if reset:
        query_params.append(('reset', "true"))
    if encrypted:
        query_params.append(('encrypted', "true"))
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(target_route, ssl=False, params=query_params) as resp:
                response = await resp.json()
                if resp.status == 200:
                    return response
                else:
                    raise HTTPException(
                        status_code=resp.status,
                        detail=str(response),
                    )
        except ClientConnectorError as client_error:
            raise HTTPException(
                status_code=404,
                detail=str(client_error),
            )


@router.get("/connect_initial")
async def initial_connect_to_client_and_get_features(client_ip: str, client_port: int,
                                                     encrypted: bool = False, reset: bool = False,
                                                     # current_user: models.User = Depends(deps.get_current_active_user)
                                                     ):
    target_route = target_service_url + "sm_functions/connect_initial/"
    query_params = [('client_ip', client_ip), ('client_port', client_port), ('user_id', 0)]
    # if current_user.full_name:
    # query_params.append(('user_name', current_user.full_name))
    if reset:
        query_params.append(('reset', "true"))
    if encrypted:
        query_params.append(('encrypted', "true"))
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(target_route, ssl=False, params=query_params) as resp:
                response = await resp.json()
                if resp.status == 200:
                    return response
                else:
                    raise HTTPException(
                        status_code=resp.status,
                        detail=str(response),
                    )
        except ClientConnectorError as client_error:
            raise HTTPException(
                status_code=404,
                detail=str(client_error),
            )


@router.get("/discover", response_model=List[schemas.ServiceInfo])
async def discover_clients():
    target_route = target_service_url + "sm_functions/discover/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(target_route, ssl=False) as resp:
                response = await resp.json()
                if resp.status == 200:
                    return response
                else:
                    raise HTTPException(
                        status_code=resp.status,
                        detail=str(response),
                    )
    except ClientConnectorError as client_error:
        raise HTTPException(
            status_code=404,
            detail=str(client_error),
        )


@router.delete("/{service_uuid}")
async def delete_service_by_uuid(service_uuid: str, current_user: models.User = Depends(deps.get_current_active_user)):
    target_route = target_service_url + "sm_functions/delete_service/"
    query_params = [('service_uuid', service_uuid), ('user_id', current_user.id)]

    if current_user.is_superuser:
        query_params.append(('super_user', "true"))

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(target_route, ssl=False, params=query_params) as resp:
                response = await resp.json()
                if resp.status == 200:
                    return response
                else:
                    raise HTTPException(
                        status_code=resp.status,
                        detail=str(response),
                    )
    except ClientConnectorError as client_error:
        raise HTTPException(
            status_code=404,
            detail=str(client_error),
        )


@router.get("/browse", response_model=List[schemas.ServiceInfo])
async def browse_clients():
    target_route = target_service_url + "sm_functions/browse_clients/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(target_route, ssl=False) as resp:
                response = await resp.json()
                if resp.status == 200:
                    return response
                else:
                    raise HTTPException(
                        status_code=resp.status,
                        detail=str(response),
                    )
    except ClientConnectorError as client_error:
        raise HTTPException(
            status_code=404,
            detail=str(client_error),
        )


@router.put("/{service_uuid}")
async def update_service_by_uuid(service_uuid: str,
                                 update_data: Dict[str, Any] = Body(...),
                                 current_user: models.User = Depends(deps.get_current_active_user)
                                 ):
    target_route = target_service_url + "sm_functions/update_service/"
    query_params = [('service_uuid', service_uuid), ('user_id', current_user.id)]

    if current_user.is_superuser:
        query_params.append(('super_user', "true"))

    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(target_route, ssl=False, params=query_params, data=json.dumps(update_data)) as resp:
                response = await resp.json()
                if resp.status == 200:
                    return response
                else:
                    raise HTTPException(
                        status_code=resp.status,
                        detail=str(response),
                    )
    except ClientConnectorError as client_error:
        raise HTTPException(
            status_code=404,
            detail=str(client_error),
        )


@router.delete("/{service_uuid}")
async def delete_service_by_uuid(service_uuid: str, current_user: models.User = Depends(deps.get_current_active_user)):
    target_route = target_service_url + "sm_functions/delete_service/"
    query_params = [('service_uuid', service_uuid), ('user_id', current_user.id)]

    if current_user.is_superuser:
        query_params.append(('super_user', "true"))

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(target_route, ssl=False, params=query_params) as resp:
                response = await resp.json()
                if resp.status == 200:
                    return response
                else:
                    raise HTTPException(
                        status_code=resp.status,
                        detail=str(response),
                    )
    except ClientConnectorError as client_error:
        raise HTTPException(
            status_code=404,
            detail=str(client_error),
        )


@router.get("/browse_features", response_model=List[schemas.Feature])
async def browse_features(service_uuid: str):
    target_route = target_service_url + "sm_functions/browse_features/"
    query_params = [('service_uuid', service_uuid)]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(target_route, ssl=False, params=query_params) as resp:
                response = await resp.json()
            if resp.status == 200:
                return response
            else:
                raise HTTPException(
                    status_code=resp.status,
                    detail=str(response),
                )
    except ClientConnectorError as client_error:
        raise HTTPException(
            status_code=404,
            detail=str(client_error),
        )


@router.get("/disconnect")
async def disconnect_client(service_uuid: str):
    target_route = target_service_url + "sm_functions/disconnect/"
    query_params = [('service_uuid', service_uuid)]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(target_route, ssl=False, params=query_params) as resp:
                response = await resp.json()
            if resp.status == 200:
                return response
            else:
                raise HTTPException(
                    status_code=resp.status,
                    detail=str(response),
                )
    except ClientConnectorError as client_error:
        raise HTTPException(
            status_code=404,
            detail=str(client_error),
        )


@router.post("/unobservable", response_model=schemas.FunctionResponse)
async def run_unobservable(service_uuid: str,
                           feature_identifier: str,
                           function_identifier: str,
                           response_identifiers: Optional[List[str]] = Query(None),
                           parameters: Optional[List[Union[str, int, float, Any]]] = Query(None),
                           named_parameters: Optional[Dict[str, Any]] = Body(None)):
    target_route = target_service_url + "sm_functions/unobservable/"
    query_params = [('service_uuid', service_uuid), ('feature_identifier', feature_identifier),
                    ('function_identifier', function_identifier)]
    if parameters and named_parameters:
        raise HTTPException(
            status_code=400,
            detail=str("Illegal Method Call: Can not mix named and unnamed parameters"),
        )

    if response_identifiers:
        for response_id in response_identifiers:
            query_params.append(('response_identifiers', response_id))

    if parameters:
        for param in parameters:
            query_params.append(('parameters', param))

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(target_route, ssl=False, params=query_params,
                                    data=json.dumps(named_parameters) if named_parameters else None) as resp:
                response = await resp.json()
            if resp.status == 200:
                return response
            else:
                raise HTTPException(
                    status_code=resp.status,
                    detail=str(response),
                )
    except ClientConnectorError as client_error:
        raise HTTPException(
            status_code=404,
            detail=str(client_error),
        )


@router.post("/start_observable", response_model=str)  # UUID
async def start_observable(service_uuid: str,
                           feature_identifier: str,
                           function_identifier: str,
                           named_parameters: Optional[Dict[str, Any]] = Body(None),
                           response_identifiers: Optional[List[str]] = Query(None),
                           intermediate_identifiers: Optional[List[str]] = Query(None)
                           ) -> str:  # returns execution  UUID
    """ Registers observable in observables dict and forwards request to service manager """
    target_route = target_service_url + "sm_functions/observable/"
    query_params = [('service_uuid', service_uuid), ('feature_identifier', feature_identifier),
                    ('function_identifier', function_identifier)]
    if response_identifiers:
        for response_id in response_identifiers:
            query_params.append(('response_identifiers', response_id))

    if intermediate_identifiers:
        for intermediate_id in intermediate_identifiers:
            query_params.append(('intermediate_identifiers', intermediate_id))

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(target_route, ssl=False, params=query_params,
                                    data=json.dumps(named_parameters) if named_parameters else None) as resp:
                response = await resp.json()
            if resp.status == 200:
                await websocket_buffer.register_observable(execution_uuid=response)
                return response
            else:
                raise HTTPException(
                    status_code=resp.status,
                    detail=str(response),
                )
    except ClientConnectorError as client_error:
        raise HTTPException(
            status_code=404,
            detail=str(client_error),
        )


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, execution_uuid: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[execution_uuid] = websocket

    async def disconnect(self, execution_uuid: str):
        print(f'Disconnect websocket with execution_uuid {execution_uuid}')
        await self.active_connections[execution_uuid].close()
        self.active_connections.pop(execution_uuid)

    async def send_response(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def receive_message(self, websocket: WebSocket):
        return await websocket.receive_json()


manager = ConnectionManager()


@router.websocket("/ws/subscribe_observable/{execution_uuid}")
async def websocket_endpoint(websocket: WebSocket, execution_uuid: str):
    print(f'Received observable command request for uuid: {execution_uuid}', flush=True)
    await manager.connect(execution_uuid, websocket)
    try:
        """ Serve websocket for observable commands """
        async with aiohttp.ClientSession().ws_connect(
                target_service_ws_url + f'sm_functions/ws/observable/{execution_uuid}') as ws:
            await ws.send_str(execution_uuid)
            # Start streaming
            while True:
                try:
                    resp = await ws.receive_json()
                    print(resp)

                    # Put results in buffer queue
                    await manager.send_response(json.dumps(resp, sort_keys=True, default=str), websocket)
                    # websocket_buffer.observables_dict[execution_uuid].put(resp)
                    if execution_uuid in resp.keys():
                        if resp[execution_uuid]["response"]:
                            await manager.disconnect(execution_uuid)
                            break
                    elif 'status_code' in resp.keys():
                        await manager.disconnect(execution_uuid)
                        break
                except (TypeError, KeyError):
                    err_msg = {'status_code': 404,
                               'message': f'No observable with execution_uuid {execution_uuid}'}
                    await manager.send_response(json.dumps(err_msg, sort_keys=True, default=str), websocket)
                    await manager.disconnect(execution_uuid)
                    await ws.close()
                    break

    except (WebSocketDisconnect, ConnectionClosedError):
        # client_controller.disconnect_websocket(execution_uuid)
        await manager.disconnect(execution_uuid)
    except ConnectionClosedOK:
        pass
    return


@router.get("/stop_observable")  # UUID
async def stop_observable(execution_uuid: str):  # returns execution  UUID
    """ Registers observable in observables dict and instantiates SiLA Python client for observable """
    target_route = target_service_url + "sm_functions/stop_observable"
    query_params = [('execution_uuid', execution_uuid)]

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(target_route, ssl=False, params=query_params) as resp:
                response = await resp.json()
                if resp.status == 204:
                    return True
                else:
                    raise HTTPException(
                        status_code=resp.status,
                        detail=str(response),
                    )
        except ClientConnectorError as client_error:
            raise HTTPException(
                status_code=404,
                detail=str(client_error),
            )
