"""Module defining the classes with query common attributes."""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Type, get_origin

from pydantic import BaseModel, Field, create_model, root_validator, validator
from pydantic.fields import SHAPE_LIST

from app.models import BaseNode, BaseNodeQuery


class SchemaSize(BaseModel):
    """Model to add query attribute related to data response size.

    Attributes:
    ----------
        with_conn (bool): Show related items.
    """

    with_conn: bool = Field(default=False, description="Show related items.")


class Pagination(BaseModel):
    """Model to filter lists in GET operations with multiple items.

    Attributes:
    ----------
        page (int): Divide the list in chunks.
        size (int | None): Chunk size.
    """

    page: int = Field(default=0, description="Divide the list in chunks")
    size: Optional[int] = Field(default=None, description="Chunk size.")

    @root_validator(pre=True)
    def set_page_to_0(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """If chunk size is 0 set page index to 0."""
        if values.get("size") is None:
            values["page"] = 0
        return values


class DbQueryCommonParams(BaseModel):
    """Model to read common query attributes passed to GET operations.

    Attributes:
    ----------
        skip (int): Number of items to skip from the first one in the list.
        limit (int | None): Maximum number or returned items.
        sort (str | None): Sorting rule.
    """

    skip: int = Field(
        default=0, description="Number of items to skip from the first one in the list."
    )
    limit: Optional[int] = Field(
        default=None, description="Maximum number or returned items."
    )
    sort: Optional[str] = Field(default=None, description="Sorting rule.")

    @validator("sort")
    def parse_sort_rule(cls, v: Optional[str]) -> Dict[str, Any]:
        """Parse and correct sort rule.

        Remove `_asc` or `_desc` suffix. Prepend `-` when `_desc` is received.
        """
        if v is None:
            return v

        if v.endswith("_asc"):
            return v[: -len("_asc")]
        elif v.endswith("_desc"):
            return v[: -len("_desc")]
        return v


def create_query_model(
    model_name: str, base_model: Type[BaseNode]
) -> Type[BaseNodeQuery]:
    """Create a Query Model from Base Model.

    The new model has the given model name.
    It has the same attributes as the Base model plus attributes used to execute filters
    and queries on the database.
    Convert to None the default value for all attributes.

    Args:
    ----
        model_name (str): New model name.
        base_model (Type[BaseNode]): Input base model from which retrieve the
            attributes.

    Returns:
    -------
        Type[BaseNodeQuery].
    """
    d = {}
    for k, v in base_model.__fields__.items():
        if get_origin(v.type_):
            continue
        if v.shape == SHAPE_LIST:
            continue
        elif issubclass(v.type_, bool):
            d[k] = (Optional[v.type_], None)
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
            d[f"{k}__lt"] = t
            d[f"{k}__gt"] = t
            d[f"{k}__lte"] = t
            d[f"{k}__gte"] = t
            d[f"{k}__ne"] = t
        else:
            d[k] = (Optional[v.type_], None)
    return create_model(model_name, __base__=BaseNodeQuery, **d)


def create_subquery_model(base_model: BaseNodeQuery):
    """Create Query Model starting from another Query Model."""
    d = {}
    for k, v in base_model.__fields__.items():
        d[f"service_{k}"] = (v.type_, v.default)
    name = base_model.__qualname__.replace("Query", "SubQuery")
    return create_model(name, **d)
