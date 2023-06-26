import uvicorn
from fastapi import FastAPI
from neomodel import config

from .cluster.api.router import router as cluster_router
from .flavor.api.router import router as flavor_router
from .identity_provider.api.router import router as identity_provider_router
from .image.api.router import router as image_router
from .location.api.router import router as location_router
from .project.api.router import router as project_router
from .provider.api.router import router as provider_router
from .quota.api.router import router as quota_router
from .quota_type.api.router import router as quota_type_router
from .service.api.router import router as service_router
from .service_type.api.router import router as service_type_router
from .sla.api.router import router as sla_router
from .user_group.api.router import router as user_group_router


config.DATABASE_URL = "bolt://neo4j:password@localhost:7687"

app = FastAPI()
app.include_router(cluster_router)
app.include_router(flavor_router)
app.include_router(identity_provider_router)
app.include_router(image_router)
app.include_router(location_router)
app.include_router(project_router)
app.include_router(provider_router)
app.include_router(quota_router)
app.include_router(quota_type_router)
app.include_router(service_router)
app.include_router(service_type_router)
app.include_router(sla_router)
app.include_router(user_group_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
