"""Core pydantic models."""

from datetime import date, datetime
from enum import Enum
from typing import Any, Literal, get_origin
from uuid import UUID

from neo4j.time import Date, DateTime
from neomodel import One, OneOrMore, ZeroOrMore, ZeroOrOne
from pydantic import BaseModel, Field, create_model, fields, validator
from pydantic.fields import SHAPE_LIST

DOC_SCHEMA_TYPE = "Inner attribute to distinguish between schema types"


class BaseNode(BaseModel):
    """Common attributes and validators for a schema of a generic neo4j Node.

    Add description field and a validator converting UUIDs to str.

    Attributes:
    ----------
        description (str): Brief item description
    """

    description: str = Field(default="", description="Brief item description")

    @validator("*", pre=True, always=True)
    @classmethod
    def not_none(cls, v: Any, field: fields.ModelField) -> Any:
        """Before any check, return the default value if the field is None."""
        if all((getattr(field, "default", None) is not None, v is None)):
            return field.default
        else:
            return v

    @validator("*", pre=True, always=True)
    @classmethod
    def get_str_from_uuid(cls, v: Any, field: fields.ModelField) -> Any:
        """Get hex attribute from UUID values."""
        if field.shape == fields.SHAPE_LIST and not isinstance(
            v, (OneOrMore, ZeroOrMore)
        ):
            return [i.hex if isinstance(i, UUID) else i for i in v]
        return v.hex if isinstance(v, UUID) else v

    @validator("*", always=True)
    @classmethod
    def get_value_from_enums(cls, v: Any) -> Any:
        """Get value from all the enumeration field values."""
        return v.value if isinstance(v, Enum) else v


class BaseNodeCreate(BaseModel):
    """Common validator when updating or creating a node in the DB.

    When dealing with enumerations retrieve the enum value.
    Always validate assignments.
    """

    class Config:
        """Sub class to validate assignments."""

        validate_assignment = True


class BaseNodeRead(BaseModel):
    """Common attributes and validators when reading nodes from the DB.

    Use ORM mode to read data from DB models.
    Add the uid attribute.
    Convert Neo4j datetime objects into python
    datetime ones.
    When dealing with relationships retrieve all connected items and show
    them as an object list. If a relationships has a model return a dict with the data
    stored in it.
    Always validate assignments.

    Attributes:
    ----------
        uid (str): Database item's unique identifier.
    """

    uid: str = Field(description="Database item's unique identifier.")

    @validator("*", pre=True)
    @classmethod
    def get_relationships(cls, v: Any) -> Any:
        """Cast neomodel relationships to lists.

        From One or ZeroOrOne relationships get that single relationship.
        From OneOrMore or ZeroOrMore relationships get all relationships.

        If the relationship has a model, return a dict with the data stored in the
        relationship.
        """
        if isinstance(v, (One, ZeroOrOne)):
            if v.definition.get("model") is None:
                return v.single()
            node = v.single()
            if node is not None:
                item = node.__dict__
                item["relationship"] = v.relationship(node)
                return item
            return node
        if isinstance(v, (OneOrMore, ZeroOrMore)):
            if v.definition.get("model") is None:
                return v.all()
            items = []
            for node in v.all():
                item = node.__dict__
                item["relationship"] = v.relationship(node)
                items.append(item)
            return items
        return v

    @validator("*", pre=True)
    @classmethod
    def cast_neo4j_datetime_or_date(cls, v: Any) -> Any:
        """Cast neo4j datetime to python datetime or date."""
        if isinstance(v, (Date, DateTime)):
            return v.to_native()
        return v

    class Config:
        """Sub class to validate assignments and enable orm mode."""

        validate_assignment = True
        orm_mode = True


class BaseReadPublic(BaseModel):
    """Add the internal schema_type attribute."""

    schema_type: Literal["public"] = Field(
        default="public", description=DOC_SCHEMA_TYPE
    )


class BaseReadPrivate(BaseModel):
    """Add the internal schema_type attribute."""

    schema_type: Literal["private"] = Field(
        default="private", description=DOC_SCHEMA_TYPE
    )


class BaseReadPublicExtended(BaseModel):
    """Add the internal schema_type attribute."""

    schema_type: Literal["public_extended"] = Field(
        default="public_extended", description=DOC_SCHEMA_TYPE
    )


class BaseReadPrivateExtended(BaseModel):
    """Add the internal schema_type attribute."""

    schema_type: Literal["private_extended"] = Field(
        default="private_extended", description=DOC_SCHEMA_TYPE
    )


class BaseNodeQuery(BaseModel):
    """Schema used to retrieve possible query parameters when performing GET operations.

    Always validate assignments.
    """

    class Config:
        """Sub class to validate assignments."""

        validate_assignment = True


def create_query_model(
    model_name: str, base_model: type[BaseNode]
) -> type[BaseNodeQuery]:
    """Create a Query Model from Base Model.

    The new model has the given model name.
    It has the same attributes as the Base model plus attributes used to execute filters
    and queries on the database.
    Convert to None the default value for all attributes.

    Args:
    ----
        model_name (str): New model name.
        base_model (type[BaseNode]): Input base model from which retrieve the
            attributes.

    Returns:
    -------
        type[BaseNodeQuery].
    """
    d = {}
    for k, v in base_model.__fields__.items():
        if get_origin(v.type_):
            continue
        if v.shape == SHAPE_LIST:
            continue
        elif issubclass(v.type_, bool):
            d[k] = (v.type_ | None, None)
        elif issubclass(v.type_, str) or issubclass(v.type_, Enum):
            t = (str | None, None)
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
            t = (int | None, None)
            d[k] = t
            d[f"{k}__lt"] = t
            d[f"{k}__gt"] = t
            d[f"{k}__lte"] = t
            d[f"{k}__gte"] = t
            d[f"{k}__ne"] = t
        elif issubclass(v.type_, float):
            t = (float | None, None)
            d[k] = t
            d[f"{k}__lt"] = t
            d[f"{k}__gt"] = t
            d[f"{k}__lte"] = t
            d[f"{k}__gte"] = t
            d[f"{k}__ne"] = t
        elif issubclass(v.type_, datetime):
            t = (datetime | None, None)
            d[f"{k}__lt"] = t
            d[f"{k}__gt"] = t
            d[f"{k}__lte"] = t
            d[f"{k}__gte"] = t
            d[f"{k}__ne"] = t
        elif issubclass(v.type_, date):
            t = (date | None, None)
            d[f"{k}__lt"] = t
            d[f"{k}__gt"] = t
            d[f"{k}__lte"] = t
            d[f"{k}__gte"] = t
            d[f"{k}__ne"] = t
        else:
            d[k] = (v.type_ | None, None)
    return create_model(model_name, __base__=BaseNodeQuery, **d)
