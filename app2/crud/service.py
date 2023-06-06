from uuid import UUID
from neo4j import ManagedTransaction
from typing import List, Optional

from ..schemas import Service


def create_service(
    tx: ManagedTransaction, sla_id: UUID, *args, **kwargs
) -> Service:
    s = ", ".join(
        [f"n.{k}=${k}" for k in Service.__fields__.keys() if k != "id"]
    )
    name = kwargs.pop("name")
    if name is not None:
        name = name.value
    resource_type = kwargs.pop("resource_type")
    if resource_type is not None:
        resource_type = resource_type.value
    cypher = "MATCH (p:SLA {id: $sla_id}) "
    cypher += "MERGE (n:Service {id: apoc.create.uuid()}) "
    cypher += f"SET {s} "
    cypher += "MERGE (n)-[r:BELONGS_TO]->(p)"
    cypher += "RETURN n"
    result = tx.run(
        cypher,
        sla_id=str(sla_id),
        name=name,
        resource_type=resource_type,
        *args,
        **kwargs,
    )
    return result.single(strict=True).data().get("n")


def get_services(tx: ManagedTransaction, *args, **kwargs) -> List[Service]:
    cypher = """
        MATCH (n:Service)
        RETURN n
    """
    result = tx.run(cypher, *args, **kwargs)
    return [record.data().get("n") for record in result]


def get_service(tx: ManagedTransaction, id: UUID) -> Optional[Service]:
    cypher = """
        MATCH (n:Service {id: $id})
        RETURN n
    """
    result = tx.run(cypher, id=str(id))
    result = result.single()
    if result is None:
        return result
    return result.data().get("n")


def get_service_by_name(tx: ManagedTransaction, name: str) -> Service:
    cypher = """
        MATCH (n:Service {name: $name})
        RETURN n
    """
    result = tx.run(cypher, name=name)
    result = result.single()
    if result is None:
        return result
    return result.data().get("n")


def remove_service(tx: ManagedTransaction, id: UUID) -> None:
    cypher = """
        MATCH (n:Service {id: $id})
        DETACH DELETE n
    """
    result = tx.run(cypher, id=str(id))
    return result.single() is None
