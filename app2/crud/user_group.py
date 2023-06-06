from uuid import UUID
from neo4j import ManagedTransaction
from typing import List, Optional

from ..schemas import UserGroup


def create_user_group(tx: ManagedTransaction, *args, **kwargs) -> UserGroup:
    s = ", ".join(
        [f"n.{k}=${k}" for k in UserGroup.__fields__.keys() if k != "id"]
    )
    cypher = "MERGE (n:UserGroup {id: apoc.create.uuid()}) "
    cypher += f"SET {s} "
    cypher += "RETURN n"
    result = tx.run(cypher, *args, **kwargs)
    return result.single(strict=True).data().get("n")


def get_user_groups(
    tx: ManagedTransaction, *args, **kwargs
) -> List[UserGroup]:
    cypher = """
        MATCH (n:UserGroup)
        RETURN n
    """
    result = tx.run(cypher, *args, **kwargs)
    return [record.data().get("n") for record in result]


def get_user_group(tx: ManagedTransaction, id: UUID) -> Optional[UserGroup]:
    cypher = """
        MATCH (n:UserGroup {id: $id})
        RETURN n
    """
    result = tx.run(cypher, id=str(id))
    result = result.single()
    if result is None:
        return result
    return result.data().get("n")


def get_user_group_by_name(tx: ManagedTransaction, name: str) -> UserGroup:
    cypher = """
        MATCH (n:UserGroup {name: $name})
        RETURN n
    """
    result = tx.run(cypher, name=name)
    result = result.single()
    if result is None:
        return result
    return result.data().get("n")


def remove_user_group(tx: ManagedTransaction, id: UUID) -> None:
    cypher = """
        MATCH (n:UserGroup {id: $id})
        DETACH DELETE n
    """
    result = tx.run(cypher, id=str(id))
    return result.single() is None
