from enum import StrEnum
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Union, List


class ServiceType(StrEnum):
    OS_NOVA = "org.openstack.nova"


class IdentityProvider(BaseModel):
    issuer: str


class Service(BaseModel):
    type: ServiceType
    provider: str
    endpoint: str
    description: Union[str, None] = None
    idps: List[IdentityProvider]


class ServiceDAO:
    def __init__(self, driver):
        self.driver = driver

    def all(self):
        def get_services(tx):
            cypher = """
                        MATCH (s:Service)
                        RETURN s AS service
            """
            result = tx.run(cypher)
            return [row.value("service") for row in result]

        return self.driver.read(get_services)

    def find_by_id(self, id):
        def get_service(tx, *args, **kwargs):
            cypher = """
                        MATCH (s:Service {id : $id})
                        RETURN p
            """
            result = tx.run(cypher, *args, **kwargs).single()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="No service with the provided id found in the database."
                )
            return result.value()

        return self.driver.read(get_service, id=id)

    def add(self, service: Service):
        # todo: review the following queries
        def add_service(tx, *args, **kwargs):
            idps = [m.dict() for m in kwargs["idps"]]
            kwargs["idps"] = idps
            cypher = """
                        MATCH (p:Provider {name: $provider})
                        MERGE (s:Service {endpoint: $endpoint})
                        SET s.description = $description, s.type = $type
                        MERGE (s)-[r:BELONGS_TO]->(p)
                        RETURN s
            """
            result = tx.run(cypher, *args, **kwargs).data()
            print(result)
            if not result:
                raise HTTPException(
                    status_code=400,
                    detail="No provider with the provided name found in the database."
                )
            cypher = """
                MATCH (s:Service {endpoint: $endpoint})
                UNWIND $idps AS idp
                WITH idp
                MERGE (i:IdentityProvider {issuer: idp.issuer})
                MERGE (s)-[auth:SUPPORTS]->(i)
                RETURN s
            """
            result = tx.run(cypher, *args, **kwargs).single()
            return result

        return self.driver.write(add_service,
                                 provider=service.provider,
                                 endpoint=service.endpoint,
                                 type=service.type,
                                 description=service.description,
                                 idps=service.idps
                                 )

    def remove(self, id):
        def remove_service(tx, *args, **kwargs):
            cypher = """
                        MATCH (s:Service {id : $id})
                        DETACH DELETE p
            """
            result = tx.run(cypher, *args, **kwargs)
            return result

        return self.driver.write(remove_service, id=id)
