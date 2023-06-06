from uuid import UUID
from neo4j import ManagedTransaction
from typing import List, Optional

from ..schemas import SLA


def create_sla(
    tx: ManagedTransaction,
    project_id: UUID,
    provider_id: UUID,
    *args,
    **kwargs,
) -> SLA:
    s = ", ".join([f"n.{k}=${k}" for k in SLA.__fields__.keys() if k != "id"])
    cypher = "MATCH (p1:Provider {id: $provider_id}), (p2:Project {id: $project_id}) "
    cypher += "MERGE (n:SLA {id: apoc.create.uuid()}) "
    cypher += f"SET {s} "
    cypher += "MERGE (p2)-[r2:REQUIRES_RESOURCES]->(n)-[r1:CAN_ACCESS_TO]->(p1) "
    cypher += "RETURN n"
    result = tx.run(
        cypher,
        project_id=str(project_id),
        provider_id=str(provider_id),
        *args,
        **kwargs,
    )
    return result.single(strict=True).data().get("n")


def get_slas(tx: ManagedTransaction, *args, **kwargs) -> List[SLA]:
    cypher = """
        MATCH (n:SLA)
        RETURN n
    """
    result = tx.run(cypher, *args, **kwargs)
    return [record.data().get("n") for record in result]


def get_sla(tx: ManagedTransaction, id: UUID) -> Optional[SLA]:
    cypher = """
        MATCH (n:SLA {id: $id})
        RETURN n
    """
    result = tx.run(cypher, id=str(id))
    result = result.single()
    if result is None:
        return result
    return result.data().get("n")


def get_sla_by_name(tx: ManagedTransaction, name: str) -> SLA:
    cypher = """
        MATCH (n:SLA {name: $name})
        RETURN n
    """
    result = tx.run(cypher, name=name)
    result = result.single()
    if result is None:
        return result
    return result.data().get("n")


def remove_sla(tx: ManagedTransaction, id: UUID) -> None:
    cypher = """
        MATCH (n:SLA {id: $id})
        DETACH DELETE n
    """
    result = tx.run(cypher, id=str(id))
    return result.single() is None
