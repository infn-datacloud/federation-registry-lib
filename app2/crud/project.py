from uuid import UUID
from neo4j import ManagedTransaction
from typing import List, Optional

from ..schemas import Project


def create_project(
    tx: ManagedTransaction, user_group_id: UUID, *args, **kwargs
) -> Project:
    s = ", ".join(
        [f"n.{k}=${k}" for k in Project.__fields__.keys() if k != "id"]
    )
    cypher = "MATCH (p:UserGroup {id: $user_group_id}) "
    cypher += "MERGE (n:Project {id: apoc.create.uuid()}) "
    cypher += f"SET {s} "
    cypher += "MERGE (p)-[r:HAS_ACCESS_TO]->(n)"
    cypher += "RETURN n"
    result = tx.run(cypher, user_group_id=str(user_group_id), *args, **kwargs)
    return result.single(strict=True).data().get("n")


def get_projects(tx: ManagedTransaction, *args, **kwargs) -> List[Project]:
    cypher = """
        MATCH (n:Project)
        RETURN n
    """
    result = tx.run(cypher, *args, **kwargs)
    return [record.data().get("n") for record in result]


def get_project(tx: ManagedTransaction, id: UUID) -> Optional[Project]:
    cypher = """
        MATCH (n:Project {id: $id})
        RETURN n
    """
    result = tx.run(cypher, id=str(id))
    result = result.single()
    if result is None:
        return result
    return result.data().get("n")


def get_project_by_name(tx: ManagedTransaction, name: str) -> Project:
    cypher = """
        MATCH (n:Project {name: $name})
        RETURN n
    """
    result = tx.run(cypher, name=name)
    result = result.single()
    if result is None:
        return result
    return result.data().get("n")


def remove_project(tx: ManagedTransaction, id: UUID) -> None:
    cypher = """
        MATCH (n:Project {id: $id})
        DETACH DELETE n
    """
    result = tx.run(cypher, id=str(id))
    return result.single() is None
