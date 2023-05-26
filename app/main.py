import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import v1
from .neo4jdb import Neo4jConnection

app = FastAPI()


@app.exception_handler(AttributeError)
async def attribute_error_exception_handler(request: Request, exc: AttributeError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


with open("config.json") as f:
    config = json.load(f)
    setattr(app, "config", config)

db = Neo4jConnection(
    uri=app.config.get("NEO4J_URI"),
    user=app.config.get("NEO4J_USER"),
    pwd=app.config.get("NEO4J_PWD"),
    database=app.config.get("NEO4J_DB")
)


def set_constraints(tx):
    tx.run("""
            CREATE CONSTRAINT
            Provider_name_unique IF NOT EXISTS
            FOR (p:Provider) REQUIRE p.name IS UNIQUE
        """)
    tx.run("""
                CREATE CONSTRAINT
                Service_type_endpoint_unique IF NOT EXISTS
                FOR (s:Service) REQUIRE (s.type, s.endpoint) IS UNIQUE
        """)
    tx.run("""
                CREATE CONSTRAINT
                IdentityProvider_issuer_unique IF NOT EXISTS
                FOR (i:IdentityProvider) REQUIRE i.issuer IS UNIQUE
        """)


db.write(set_constraints)

app.include_router(v1.router, prefix="/v1")

