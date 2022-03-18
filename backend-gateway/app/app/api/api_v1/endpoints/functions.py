import json
from typing import List, Optional, Union, Any, Dict

import aiohttp
from aiohttp import ClientConnectorError
from fastapi import APIRouter, Query, HTTPException, Body

from app import schemas
from app.core.config import settings

router = APIRouter()
target_service_hostname = "http://sila2_manager_service-manager_1"  # -> to env var
target_service_port = settings.SERVICE_MANAGER_UVICORN_PORT  # -> to env var
target_service_api_version = settings.API_V1_STR  # -> to env var

target_service_url = target_service_hostname + ":" \
                     + str(settings.SERVICE_MANAGER_UVICORN_PORT) \
                     + str(settings.API_V1_STR) + "/"


@router.get("/connect")
async def connect_to_client(client_ip: str, client_port: int, reset: bool = False):
    target_route = target_service_url + "sm_functions/connect/"
    query_params = [('client_ip', client_ip), ('client_port', client_port)]
    if reset:
        query_params.append(('reset', "true"))
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
async def initial_connect_to_client_and_get_features(client_ip: str, client_port: int, reset: bool = False):
    target_route = target_service_url + "sm_functions/connect_initial/"
    query_params = [('client_ip', client_ip), ('client_port', client_port)]
    if reset:
        query_params.append(('reset', "true"))
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


@router.post("/unobservable", response_model=schemas.FunctionResponse)
async def run_client_function(service_uuid: str,
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
