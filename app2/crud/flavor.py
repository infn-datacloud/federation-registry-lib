from uuid import UUID
from neo4j import ManagedTransaction
from typing import List, Optional

from ..schemas import Flavor


def create_flavor(
    tx: ManagedTransaction, project_id: UUID, *args, **kwargs
) -> Flavor:
    s = ", ".join(
        [f"n.{k}=${k}" for k in Flavor.__fields__.keys() if k != "id"]
    )
    cypher = "MATCH (p:Project {id: $project_id}) "
    cypher += "MERGE (n:Flavor {id: apoc.create.uuid()}) "
    cypher += f"SET {s} "
    cypher += "MERGE (n)-[r:BELONGS_TO]->(p)"
    cypher += "RETURN n"
    result = tx.run(cypher, project_id=str(project_id), *args, **kwargs)
    return result.single(strict=True).data().get("n")


def get_flavors(tx: ManagedTransaction, *args, **kwargs) -> List[Flavor]:
    cypher = """
        MATCH (n:Flavor)
        RETURN n
    """
    result = tx.run(cypher, *args, **kwargs)
    return [record.data().get("n") for record in result]


def get_flavor(tx: ManagedTransaction, id: UUID) -> Optional[Flavor]:
    cypher = """
        MATCH (n:Flavor {id: $id})
        RETURN n
    """
    result = tx.run(cypher, id=str(id))
    result = result.single()
    if result is None:
        return result
    return result.data().get("n")


def get_flavor_by_name(tx: ManagedTransaction, name: str) -> Flavor:
    cypher = """
        MATCH (n:Flavor {name: $name})
        RETURN n
    """
    result = tx.run(cypher, name=name)
    result = result.single()
    if result is None:
        return result
    return result.data().get("n")


def remove_flavor(tx: ManagedTransaction, id: UUID) -> None:
    cypher = """
        MATCH (n:Flavor {id: $id})
        DETACH DELETE n
    """
    result = tx.run(cypher, id=str(id))
    return result.single() is None
