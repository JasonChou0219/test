from typing import Any, List

from fastapi import APIRouter, Depends
from requests import get

from app import models
from app.api import deps
from app.core.config import settings

router = APIRouter()
target_service_hostname = "http://sila2_device_manager_data-acquisition_1"  # -> to env var
target_service_port = settings.DATA_ACQUISITION_UVICORN_PORT  # -> to env var
target_service_api_version = settings.API_V1_STR  # -> to env var

target_service_url = target_service_hostname + ":" \
                     + str(settings.DATA_ACQUISITION_UVICORN_PORT) \
                     + str(settings.API_V1_STR) + "/"


@router.get("/", response_model=List[dict])
def read_dataflows(
        current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Retrieve dataflows.
    """
    target_route = f"{target_service_url}dataflows/"
    dataflows = get(
        target_route
    ).json()

    return dataflows
