from typing import Any, List, Optional
from neomodel import StructuredNode
from pydantic import BaseModel


def truncate(
    items: List[Any], skip: int = 0, limit: Optional[int] = None
) -> List[Any]:
    if limit is None:
        return items[skip:]
    start = skip
    end = skip + limit
    return items[start:end]


def update(new_item: BaseModel, old_item: StructuredNode):
    for k, v in new_item.dict(exclude_unset=True).items():
        old_item.__setattr__(k, v)
    old_item.save()
    return old_item
