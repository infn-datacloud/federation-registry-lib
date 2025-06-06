"""Core pydantic models."""

from datetime import date, datetime
from enum import Enum
from typing import Annotated, Any, Literal, get_origin
from uuid import UUID

from neo4j.time import Date, DateTime
from neomodel import One, OneOrMore, ZeroOrMore, ZeroOrOne
from pydantic import BaseModel, Field, create_model, fields, validator
from pydantic.fields import SHAPE_LIST

DOC_SCHEMA_TYPE = "Inner attribute to distinguish between schema types"
MAX_DEEP = 1


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
    Add the id attribute.
    Convert Neo4j datetime objects into python
    datetime ones.
    When dealing with relationships retrieve all connected items and show
    them as an object list. If a relationships has a model return a dict with the data
    stored in it.
    Always validate assignments.

    Attributes:
    ----------
        id (str): Database item's unique identifier.
    """

    id: Annotated[str, Field(description="Database item's unique identifier.")]

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


def get_field_basic_type(field_type: Any) -> tuple[Any, None] | None:
    """Return the new field basic type based on the parent field type."""
    if issubclass(field_type, bool):
        return (field_type | None, None)
    if issubclass(field_type, (str, Enum)):
        return (str | None, None)
    if issubclass(field_type, (int, float, date, datetime)):
        return (field_type | None, None)
    return None


def get_list_derived_attributes(
    new_field: tuple[Any, None] | None, field_name: str, field_type: Any, deep: int
) -> dict[str, Any]:
    """Return fields to perform queries on list fields."""
    d = {}
    if new_field is None and deep > 0:
        for sub_field in field_type.__fields__.values():
            sub_fields = add_fields(sub_field, prefix=field_name, deep=deep - 1)
            d.update(sub_fields)
        return d
    d[f"{field_name}__contains"] = new_field
    d[f"{field_name}__icontains"] = new_field
    return d


def add_fields(
    field: fields.ModelField, prefix: str = "", deep: int = 0
) -> dict[str, Any]:
    """Add fields to a dictionary."""
    d = {}
    origin = get_origin(field.type_)
    if origin is None:
        new_field = get_field_basic_type(field.type_)
    elif origin is Literal:
        return d
    else:
        # Case of typing currently not supported.
        # List, Union, Dict and similar should not be used.
        # Instead use basic types (list, dict...).
        return d

    field_name = f"{prefix}_{field.name}" if prefix != "" else field.name

    if field.shape == SHAPE_LIST:
        return get_list_derived_attributes(new_field, field_name, field.type_, deep)

    if new_field is None and deep > 0:
        for sub_field in field.type_.__fields__.values():
            sub_fields = add_fields(sub_field, prefix=field_name, deep=deep - 1)
            d.update(sub_fields)
        return d

    if issubclass(field.type_, bool):
        d[field_name] = new_field
        return d
    if issubclass(field.type_, (str, Enum)):
        d[field_name] = new_field
        d[f"{field_name}__contains"] = new_field
        d[f"{field_name}__icontains"] = new_field
        d[f"{field_name}__startswith"] = new_field
        d[f"{field_name}__istartswith"] = new_field
        d[f"{field_name}__endswith"] = new_field
        d[f"{field_name}__iendswith"] = new_field
        d[f"{field_name}__regex"] = new_field
        d[f"{field_name}__iregex"] = new_field
        return d
    if issubclass(field.type_, (int, float, date, datetime)):
        d[field_name] = new_field
        d[f"{field_name}__lt"] = new_field
        d[f"{field_name}__gt"] = new_field
        d[f"{field_name}__lte"] = new_field
        d[f"{field_name}__gte"] = new_field
        d[f"{field_name}__ne"] = new_field
        return d

    # Should never reach this point. Not covered cases.
    return d


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
    for field in base_model.__fields__.values():
        new_fields = add_fields(field, deep=MAX_DEEP)
        d.update(new_fields)
    return create_model(model_name, __base__=BaseNodeQuery, **d)
