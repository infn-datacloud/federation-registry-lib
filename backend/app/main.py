import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.dependencies import oidc_scheme
from app.config import get_settings
from app.router import router, router_v1

settings = get_settings()

dependencies = None
if settings.DISCOVERY_URL is not None:
    dependencies = [Depends(oidc_scheme)]

app = FastAPI(title=settings.PROJECT_NAME, dependencies=dependencies)

app.include_router(router, prefix="/api")
app.include_router(router_v1, prefix=f"/api{settings.API_V1_STR}")

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
