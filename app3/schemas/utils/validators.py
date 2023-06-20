from typing import List, Optional
from neomodel import RelationshipManager, StructuredNode


def get_single_node_from_rel(
    v: RelationshipManager,
) -> Optional[StructuredNode]:
    """From relationship manager return the single node"""
    if v is not None:
        return v.single()
    return v


def get_all_nodes_from_rel(
    v: RelationshipManager,
) -> Optional[List[StructuredNode]]:
    """From relationship manager return all connected nodes"""
    if v is not None:
        return v.all()
    return v
