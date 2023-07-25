import uvicorn
from fastapi import Depends, FastAPI

from app.auth.dependencies import oidc_scheme
from app.config import get_settings
from app.flavor.api.router import router as flavor_router
from app.identity_provider.api.router import router as identity_provider_router
from app.image.api.router import router as image_router
from app.location.api.router import router as location_router
from app.project.api.router import router as project_router
from app.provider.api.router import router as provider_router
from app.quota.api.router import router as quota_router
from app.service.api.router import router as service_router
from app.sla.api.router import router as sla_router
from app.user_group.api.router import router as user_group_router

settings = get_settings()

dependencies = None
if settings.DISCOVERY_URL is not None:
    dependencies = [Depends(oidc_scheme)]
app = FastAPI(dependencies=dependencies)
app.include_router(flavor_router)
app.include_router(identity_provider_router)
app.include_router(image_router)
app.include_router(location_router)
app.include_router(project_router)
app.include_router(provider_router)
app.include_router(quota_router)
app.include_router(service_router)
app.include_router(sla_router)
app.include_router(user_group_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
