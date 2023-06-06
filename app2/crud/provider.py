from uuid import UUID
from neo4j import ManagedTransaction
from typing import List, Optional

from ..schemas import Provider


def create_provider(tx: ManagedTransaction, *args, **kwargs) -> Provider:
    s = ", ".join(
        [f"p.{k}=${k}" for k in Provider.__fields__.keys() if k != "id"]
    )
    cypher = "MERGE (p:Provider {id: apoc.create.uuid()}) "
    cypher += f"SET {s} "
    cypher += "RETURN p"
    result = tx.run(cypher, *args, **kwargs)
    return result.single(strict=True).data().get("p")


def get_providers(tx: ManagedTransaction, *args, **kwargs) -> List[Provider]:
    cypher = """
        MATCH (p:Provider)
        RETURN p
    """
    result = tx.run(cypher, *args, **kwargs)
    return [record.data().get("p") for record in result]


def get_provider(tx: ManagedTransaction, id: UUID) -> Optional[Provider]:
    cypher = """
        MATCH (p:Provider {id: $id})
        RETURN p
    """
    result = tx.run(cypher, id=id)
    result = result.single()
    if result is None:
        return result
    return result.data().get("p")


def get_provider_by_name(tx: ManagedTransaction, name: str) -> Provider:
    cypher = """
        MATCH (p:Provider {name: $name})
        RETURN p
    """
    result = tx.run(cypher, name=name)
    result = result.single()
    if result is None:
        return result
    return result.data().get("p")


def remove_provider(tx: ManagedTransaction, id: UUID) -> None:
    cypher = """
        MATCH (p:Provider {id: $id})
        DETACH DELETE p
    """
    result = tx.run(cypher, id=id)
    return result.single() is None
