import aiohttp
from fastapi import APIRouter

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


@router.get("/", response_model=schemas.Feature)
async def get_feature_definition():
    target_route = target_service_url + "sm_functions/features/"
    async with aiohttp.ClientSession() as session:
        async with session.get(target_route, ssl=False) as resp:
            data = await resp.text()
            feature = Feature.parse_raw(data)
            return feature

