import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.router import router_v1

summary = """
Configuration Management Database (CMDB)
of the DataCloud project
"""
description = """
Configuration Management Database (CMDB) stores providers data
used by the DataCloud Orchestrator to deploy new services.

You can inspect providers data, identity providers user groups
and Service Level Agreement connecting these data.

This database is mainly populated by scripts.
"""
version = "0.1.0"
contact = {
    "name": "Giovanni Savarese",
    "url": "https://github.com/giosava94",
    "email": "giovanni.savarese@ba.infn.it",
}

settings = get_settings()

tags_metadata = [
    {
        "name": settings.API_V1_STR,
        "description": "API version 1, see link on the right",
        "externalDocs": {
            "description": "API version 1 documentation",
            "url": f"http://{settings.DOMAIN}/api/v1/docs",
        },
    },
]

app = FastAPI(
    contact=contact,
    description=description,
    openapi_tags=tags_metadata,
    summary=summary,
    title=settings.PROJECT_NAME,
    version=version,
)
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

sub_app_v1 = FastAPI(
    contact=contact,
    description=description,
    summary=summary,
    title=settings.PROJECT_NAME,
    version=version,
)
sub_app_v1.include_router(router_v1)
app.mount(settings.API_V1_STR, sub_app_v1)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
