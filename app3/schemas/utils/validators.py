from datetime import datetime
from enum import Enum
from typing import Optional
from neomodel import RelationshipManager, StructuredNode
from neo4j.time import DateTime


def cast_neo4j_datetime(v: DateTime) -> datetime:
    """Convert neo4j datetime to datetime"""
    if type(v) is DateTime:
        return v.to_native()
    return v


def get_enum_value(v: Enum) -> str:
    """Return the enum string value"""
    if v is not None:
        return v.value
    return v

def get_single_node_from_rel(
    v: RelationshipManager,
) -> Optional[StructuredNode]:
    """From relationship manager return the single node"""
    if v is not None:
        return v.single()
    return v