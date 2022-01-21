from typing import List

from fastapi import APIRouter

from app import schemas
from app.service_manager import client_controller

router = APIRouter()


@router.get("/connect", response_model=List[schemas.Feature])
def connect_client(client_ip: str, client_port: int):
    return client_controller.connect_client(client_ip, client_port)


@router.get("/function", response_model=schemas.Feature)
def run_function():
    client_controller
    return {"Hello": "World"}
