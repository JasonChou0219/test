from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, users, utils, jobs, scheduled_jobs, workflows

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(scheduled_jobs.router, prefix="/scheduled_jobs", tags=["scheduled_jobs"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
