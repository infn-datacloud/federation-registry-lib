import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.dependencies import oidc_scheme
from app.config import get_settings
from app.router import router_v1

settings = get_settings()

dependencies = None
if settings.DISCOVERY_URL is not None:
    dependencies = [Depends(oidc_scheme)]

tags_metadata = [
    {
        "name": settings.API_V1_STR,
        "description": "API version 1, see link on the right",
        "externalDocs": {
            "description": "API version 1 documentation",
            "url": "http://localhost:8000/api/v1/docs",
        },
    },
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    dependencies=dependencies,
    openapi_tags=tags_metadata,
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin) for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

sub_app_v1 = FastAPI(title=settings.PROJECT_NAME)
sub_app_v1.include_router(router_v1)
app.mount(settings.API_V1_STR, sub_app_v1)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
