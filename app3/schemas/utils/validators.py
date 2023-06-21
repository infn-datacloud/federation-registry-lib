from typing import List, Mapping, Optional, Union
from neomodel import StructuredNode, One, OneOrMore, ZeroOrOne, ZeroOrMore
from pydantic import BaseModel


def get_single_node_from_rel(
    v: Union[One, ZeroOrOne]
) -> Optional[StructuredNode]:
    """From relationship manager return the single node"""
    if v is not None:
        return v.single()
    return v


def get_all_nodes_from_rel(
    v: Union[OneOrMore, ZeroOrMore]
) -> Optional[List[StructuredNode]]:
    """From relationship manager return all connected nodes"""
    if v is not None:
        return v.all()
    return v


def get_all_nodes_with_rel_data(
    cls: BaseModel, v: ZeroOrMore
) -> Optional[List[Mapping]]:
    if v is not None:
        items = []
        for node in v.all():
            item = cls.from_orm(node).dict()
            item["relationship"] = v.relationship(node)
            items.append(item)
    return items
