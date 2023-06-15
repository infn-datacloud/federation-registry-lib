from pydantic import BaseModel, root_validator
from typing import Any, List, Optional


class Pagination(BaseModel):
    page: int = 0
    size: Optional[int] = None

    @root_validator(pre=True)
    def set_page_to_0(cls, values):
        if values.get("size") is None:
            values["page"] = 0
        return values


def paginate(items: List[Any], page: int, size: Optional[int]):
    if size is None:
        return items
    start = page * size
    end = start + size
    return items[start:end]
