from uuid import UUID
from neo4j import ManagedTransaction
from typing import List, Optional

from ..schemas import IdentityProvider


def create_identity_provider(
    tx: ManagedTransaction, *args, **kwargs
) -> IdentityProvider:
    s = ", ".join(
        [
            f"p.{k}=${k}"
            for k in IdentityProvider.__fields__.keys()
            if k != "id"
        ]
    )
    cypher = "MERGE (p:IdentityProvider {id: apoc.create.uuid()}) "
    cypher += f"SET {s} "
    cypher += "RETURN p"
    result = tx.run(cypher, *args, **kwargs)
    return result.single(strict=True).data().get("p")


def get_identity_providers(
    tx: ManagedTransaction, *args, **kwargs
) -> List[IdentityProvider]:
    cypher = """
        MATCH (p:IdentityProvider)
        RETURN p
    """
    result = tx.run(cypher, *args, **kwargs)
    return [record.data().get("p") for record in result]


def get_identity_provider(
    tx: ManagedTransaction, id: UUID
) -> Optional[IdentityProvider]:
    cypher = """
        MATCH (p:IdentityProvider {id: $id})
        RETURN p
    """
    result = tx.run(cypher, id=str(id))
    result = result.single()
    if result is None:
        return result
    return result.data().get("p")


def get_identity_provider_by_name(
    tx: ManagedTransaction, name: str
) -> IdentityProvider:
    cypher = """
        MATCH (p:IdentityProvider {name: $name})
        RETURN p
    """
    result = tx.run(cypher, name=name)
    result = result.single()
    if result is None:
        return result
    return result.data().get("p")


def remove_identity_provider(tx: ManagedTransaction, id: UUID) -> None:
    cypher = """
        MATCH (p:IdentityProvider {id: $id})
        DETACH DELETE p
    """
    result = tx.run(cypher, id=str(id))
    return result.single() is None
