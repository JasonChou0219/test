from fastapi import APIRouter

from app.api.api_v1.endpoints import dataflows
from app.api.api_v1.endpoints import databases
from app.api.api_v1.endpoints import protocols

api_router = APIRouter()
api_router.include_router(dataflows.router, prefix="/dataflows", tags=["dataflows"])
api_router.include_router(databases.router, prefix="/databases", tags=["databases"])
api_router.include_router(protocols.router, prefix="/protocols", tags=["protocols"])
