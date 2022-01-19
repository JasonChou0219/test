from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.SERVICE_MANAGER_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="The service manager is responsible for the SiLA Service communication. It can discover "
                "services in a local network via mDNS or in other networks through edge gateways. Requests by other "
                "servcies for the execution of SiLA commands or properties passes thorugh the servcie manager which "
                "holds dynamic clients for all available services.",
    contact={
        "name": "Lukas Bromig",
        "url": "https://www.epe.ed.tum.de/biovt/startseite/",
        "email": "lukas.bromig@tum.de",
    }
)

# Set all CORS enabled origins
if settings.SERVICE_MANAGER_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.SERVICE_MANAGER_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
from app.service_manager import auto_discovery
print(auto_discovery.find())
