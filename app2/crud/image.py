from uuid import UUID
from neo4j import ManagedTransaction
from typing import List, Optional

from ..schemas import Image


def create_image(
    tx: ManagedTransaction, project_id: UUID, *args, **kwargs
) -> Image:
    s = ", ".join(
        [f"n.{k}=${k}" for k in Image.__fields__.keys() if k != "id"]
    )
    os = kwargs.pop("os")
    if os is not None:
        os = os.value
    cypher = "MATCH (p:Project {id: $project_id}) "
    cypher += "MERGE (n:Image {id: apoc.create.uuid()}) "
    cypher += f"SET {s} "
    cypher += "MERGE (n)-[r:BELONGS_TO]->(p)"
    cypher += "RETURN n"
    result = tx.run(cypher, project_id=str(project_id), os=os, *args, **kwargs)
    return result.single(strict=True).data().get("n")


def get_images(tx: ManagedTransaction, *args, **kwargs) -> List[Image]:
    cypher = """
        MATCH (n:Image)
        RETURN n
    """
    result = tx.run(cypher, *args, **kwargs)
    return [record.data().get("n") for record in result]


def get_image(tx: ManagedTransaction, id: UUID) -> Optional[Image]:
    cypher = """
        MATCH (n:Image {id: $id})
        RETURN n
    """
    result = tx.run(cypher, id=str(id))
    result = result.single()
    if result is None:
        return result
    return result.data().get("n")


def get_image_by_name(tx: ManagedTransaction, name: str) -> Image:
    cypher = """
        MATCH (n:Image {name: $name})
        RETURN n
    """
    result = tx.run(cypher, name=name)
    result = result.single()
    if result is None:
        return result
    return result.data().get("n")


def remove_image(tx: ManagedTransaction, id: UUID) -> None:
    cypher = """
        MATCH (n:Image {id: $id})
        DETACH DELETE n
    """
    result = tx.run(cypher, id=str(id))
    return result.single() is None
