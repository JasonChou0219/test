from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="The backend gateway is responsible for authentication and authorization of all traffic. Requests from "
                "a user are forwarded to the responsible service.",
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
        # allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
