from fastapi import APIRouter

from app.api.api_v1.endpoints import services, users, utils, functions

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
api_router.include_router(functions.router, prefix="/sm_functions", tags=["functions"])
