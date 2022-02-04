import threading

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.scheduler import main as scheduler

app = FastAPI(
    title=settings.WORKFLOW_SCHEDULER_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="The workflow scheduler, aka. scheduler, allows the user to create, read, update, and delete jobs. "
                "Jobs can contain workflows, data acquisition protocols, and dataflows. The scheduler creates booking"
                "for jobs and executes them at the specified time.",
    contact={
        "name": "Lukas Bromig",
        "url": "https://www.epe.ed.tum.de/biovt/startseite/",
        "email": "lukas.bromig@tum.de",
    }
)

# Set all CORS enabled origins
if settings.BACKEND_GATEWAY_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_GATEWAY_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

# threading.Thread(target=scheduler).start()
