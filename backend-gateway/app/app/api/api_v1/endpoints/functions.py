import json
from typing import List, Optional

import aiohttp
from fastapi import APIRouter, Query

from app import schemas
from app.core.config import settings
from app.schemas import Feature

router = APIRouter()
target_service_hostname = "http://sila2_manager_service-manager_1"  # -> to env var
target_service_port = settings.SERVICE_MANAGER_UVICORN_PORT  # -> to env var
target_service_api_version = settings.API_V1_STR  # -> to env var

target_service_url = target_service_hostname + ":" \
                     + str(settings.SERVICE_MANAGER_UVICORN_PORT) \
                     + str(settings.API_V1_STR) + "/"


@router.get("/connect")
async def connect_to_client_and_get_features(client_ip: str, client_port: int):
    target_route = target_service_url + "sm_functions/connect/"
    query_params = [('client_ip', client_ip), ('client_port', client_port)]
    async with aiohttp.ClientSession() as session:
        async with session.get(target_route, ssl=False, params=query_params) as resp:
            response = await resp.json()
            return response


@router.get("/discover", response_model=List[schemas.ServiceInfo])
async def connect_to_client_and_get_features():
    target_route = target_service_url + "sm_functions/discover/"
    async with aiohttp.ClientSession() as session:
        async with session.get(target_route, ssl=False) as resp:
            response = await resp.json()
            return response


@router.get("/browse_features", response_model=List[schemas.Feature])
async def connect_to_client_and_get_features(service_uuid: str):
    target_route = target_service_url + "sm_functions/browse_features/"
    query_params = [('service_uuid', service_uuid)]
    async with aiohttp.ClientSession() as session:
        async with session.get(target_route, ssl=False, params=query_params) as resp:
            response = await resp.json()
            return response


@router.get("/function", response_model=schemas.FunctionResponse)
async def run_client_function(service_uuid: str,
                              identifier: str,
                              function: str,
                              is_property: bool,
                              is_observable: bool,
                              response_identifiers: Optional[List[str]] = Query(None),
                              parameters: Optional[List[str]] = Query(None)):
    target_route = target_service_url + "sm_functions/function/"
    query_params = [('service_uuid', service_uuid), ('identifier', identifier),
                    ('function', function), ('is_property', str(is_property)), ('is_observable', str(is_observable))]

    if response_identifiers:
        for response_id in response_identifiers:
            query_params.append(('response_identifiers', response_id))
    if parameters:
        for param in parameters:
            query_params.append(('parameters', param))

    async with aiohttp.ClientSession() as session:
        async with session.get(target_route, ssl=False, params=query_params) as resp:
            data = await resp.json()
            return data
