from fastapi import APIRouter

from app.api.api_v1.endpoints import dataflows

api_router = APIRouter()
api_router.include_router(dataflows.router, prefix="/dataflows", tags=["dataflows"])

