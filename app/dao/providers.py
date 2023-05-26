from fastapi import HTTPException
from pydantic import BaseModel
from typing import Union, List, Optional


class Provider(BaseModel):
    name: str
    description: Union[str, None] = None
    support_email: Optional[List[str]] = None


class ProviderDAO:
    def __init__(self, driver):
        self.driver = driver

    def all(self):
        def get_providers(tx):
            cypher = """
                        MATCH (p:Provider)
                        RETURN p AS provider
            """
            result = tx.run(cypher)
            return [row.value("provider") for row in result]

        return self.driver.read(get_providers)

    def find_by_id(self, id):
        def get_provider(tx, *args, **kwargs):
            cypher = """
                        MATCH (p:Provider {name : $name})
                        RETURN p
            """
            result = tx.run(cypher, *args, **kwargs).single()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="No provider with the provided name found in the database."
                )
            return result.value()

        return self.driver.read(get_provider, name=id)

    def add(self, provider: Provider):
        def add_provider(tx, *args, **kwargs):
            cypher = """
                        MERGE (p:Provider {name: $name})
                        SET p.description = $description, p.support_email = $email
                        RETURN p
            """
            result = tx.run(cypher, *args, **kwargs)
            return result.single().value()

        return self.driver.write(add_provider,
                                   name=provider.name,
                                   description=provider.description,
                                   email=provider.support_email
                                   )

    def remove(self, id):
        def remove_provider(tx, *args, **kwargs):
            cypher = """
                        MATCH (p:Provider {name : $name})
                        DETACH DELETE p
            """
            result = tx.run(cypher, *args, **kwargs)
            return result

        return self.driver.write(remove_provider, name=id)
