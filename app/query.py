from datetime import datetime
from enum import Enum
from pydantic import BaseModel, create_model, root_validator
from pydantic.fields import SHAPE_LIST
from typing import Optional

from app.models import BaseNodeQuery


class CommonGetQuery(BaseModel):
    skip: int = 0
    limit: Optional[int] = None
    sort: Optional[str] = None

    @root_validator
    def must_end_with(cls, values):
        sort_rule = values["sort"]
        if sort_rule is None:
            return values

        if sort_rule.endswith("_asc"):
            new_val = sort_rule[: -len("_asc")]
        elif sort_rule.endswith("_desc"):
            new_val = sort_rule[: -len("_desc")]
            new_val = f"-{new_val}"
        else:
            new_val = sort_rule

        values["sort"] = new_val
        return values


def create_query_model(model_name: str, base_model: BaseModel):
    d = {}
    for k, v in base_model.__fields__.items():
        if v.shape == SHAPE_LIST:
            continue
        elif issubclass(v.type_, str) or issubclass(v.type_, Enum):
            t = (Optional[str], None)
            d[k] = t
            d[f"{k}__contains"] = t
            d[f"{k}__icontains"] = t
            d[f"{k}__startswith"] = t
            d[f"{k}__istartswith"] = t
            d[f"{k}__endswith"] = t
            d[f"{k}__iendswith"] = t
            d[f"{k}__regex"] = t
            d[f"{k}__iregex"] = t
        elif issubclass(v.type_, int):
            t = (Optional[int], None)
            d[k] = t
            d[f"{k}__lt"] = t
            d[f"{k}__gt"] = t
            d[f"{k}__lte"] = t
            d[f"{k}__gte"] = t
            d[f"{k}__ne"] = t
        elif issubclass(v.type_, float):
            t = (Optional[float], None)
            d[k] = t
            d[f"{k}__lt"] = t
            d[f"{k}__gt"] = t
            d[f"{k}__lte"] = t
            d[f"{k}__gte"] = t
            d[f"{k}__ne"] = t
        elif issubclass(v.type_, datetime):
            t = (Optional[datetime], None)
            d[k] = t
            d[f"{k}__lt"] = t
            d[f"{k}__gt"] = t
            d[f"{k}__lte"] = t
            d[f"{k}__gte"] = t
            d[f"{k}__ne"] = t
        else:
            d[k] = (Optional[v.type_], None)
    return create_model(model_name, __base__=BaseNodeQuery, **d)
