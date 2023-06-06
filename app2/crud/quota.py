from uuid import UUID
from neo4j import ManagedTransaction
from typing import List, Optional

from ..schemas import Quota


def create_quota(
    tx: ManagedTransaction, sla_id: UUID, *args, **kwargs
) -> Quota:
    s = ", ".join(
        [f"n.{k}=${k}" for k in Quota.__fields__.keys() if k != "id"]
    )
    name = kwargs.pop("name")
    if name is not None:
        name = name.value
    unit = kwargs.pop("unit")
    if unit is not None:
        unit = unit.value
    cypher = "MATCH (p:SLA {id: $sla_id}) "
    cypher += "MERGE (n:Quota {id: apoc.create.uuid()}) "
    cypher += f"SET {s} "
    cypher += "MERGE (p)-[r:HAS_RESOURCE_RESTRICTIONS]->(n)"
    cypher += "RETURN n"
    result = tx.run(
        cypher, sla_id=str(sla_id), name=name, unit=unit, *args, **kwargs
    )
    return result.single(strict=True).data().get("n")


def get_quotas(tx: ManagedTransaction, *args, **kwargs) -> List[Quota]:
    cypher = """
        MATCH (n:Quota)
        RETURN n
    """
    result = tx.run(cypher, *args, **kwargs)
    return [record.data().get("n") for record in result]


def get_quota(tx: ManagedTransaction, id: UUID) -> Optional[Quota]:
    cypher = """
        MATCH (n:Quota {id: $id})
        RETURN n
    """
    result = tx.run(cypher, id=str(id))
    result = result.single()
    if result is None:
        return result
    return result.data().get("n")


def get_quota_by_name(tx: ManagedTransaction, name: str) -> Quota:
    cypher = """
        MATCH (n:Quota {name: $name})
        RETURN n
    """
    result = tx.run(cypher, name=name)
    result = result.single()
    if result is None:
        return result
    return result.data().get("n")


def remove_quota(tx: ManagedTransaction, id: UUID) -> None:
    cypher = """
        MATCH (n:Quota {id: $id})
        DETACH DELETE n
    """
    result = tx.run(cypher, id=str(id))
    return result.single() is None
