from typing import Any, List

from fastapi import APIRouter

from app import schemas, crud
from app.core.config import settings

router = APIRouter()
target_service_hostname = "http://sila2_device_manager_service-manager"  # -> to env var
target_service_port = settings.SERVICE_MANAGER_UVICORN_PORT  # -> to env var
target_service_api_version = settings.API_V1_STR  # -> to env var

target_service_url = target_service_hostname + ":" \
                     + str(settings.SERVICE_MANAGER_UVICORN_PORT) \
                     + str(settings.API_V1_STR) + "/"


@router.get("/", response_model=List[schemas.ServiceBase])
def discover_services(
) -> Any:

    print(workflows)
    return workflows
