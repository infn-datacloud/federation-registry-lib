import uvicorn
from fastapi import FastAPI
from neomodel import config

from . import routers

config.DATABASE_URL = "bolt://neo4j:password@localhost:7687"

app = FastAPI()
#app.include_router(routers.flavors_router)
app.include_router(routers.identity_providers_router)
#app.include_router(routers.images_router)
app.include_router(routers.projects_router)
app.include_router(routers.providers_router)
#app.include_router(routers.quotas_router)
#app.include_router(routers.services_router)
#app.include_router(routers.slas_router)
app.include_router(routers.user_groups_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
