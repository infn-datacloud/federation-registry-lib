from enum import Enum
from typing import Dict, Optional

from neo4j.data import DateTime
from neomodel import One, OneOrMore, ZeroOrMore, ZeroOrOne
from pydantic import UUID4, BaseModel, Field, root_validator, validator


class BaseNodeCreate(BaseModel):
    """Base Model when updating or creating a node in the DB.

    When dealing with enumerations retrieve the enum value. Always
    validate assignments.
    """

    __hash__ = object.__hash__

    description: Optional[str] = Field(default="", description="Brief item description")

    @validator("description")
    def set_empty_string(cls, desc):
        if desc is None:
            return ""

    @root_validator
    def get_value_from_enums(cls, data: Dict) -> Dict:
        """Get value from all the enumeration field values."""
        enumeration_fields = {
            k: v.value for k, v in data.items() if isinstance(v, Enum)
        }
        return {**data, **enumeration_fields}

    class Config:
        validate_assignment = True


class BaseNodeRead(BaseModel):
    """Base Model when reading nodes from the DB.

    Use ORM mode to read data from DB models. Convert Neo4j datetime
    objects into python datetime ones. When dealing with relationships
    retrieve all connected items and show them as an object list. If a
    relationships has a model return a dict with the data stored in it.
    Always validate assignments.
    """

    uid: UUID4 = Field(description="Database item's unique identifier")
    description: str = Field(default="", description="Brief item description")

    @root_validator(pre=True)
    def get_relations(cls, data: Dict) -> Dict:
        """From One or ZeroOrOne relationships get that single relationship.

        From OneOrMore or ZeroOrMore relationships get all
        relationships; if that relationships has a model return a dict
        with the data stored in the relationship.
        """
        relations = {}
        for k, v in data.items():
            if isinstance(v, One) or isinstance(v, ZeroOrOne):
                relations[k] = v.single()
            elif isinstance(v, OneOrMore) or isinstance(v, ZeroOrMore):
                if v.definition.get("model") is None:
                    relations[k] = v.all()
                else:
                    items = []
                    for node in v.all():
                        item = node.__dict__
                        item["relationship"] = v.relationship(node)
                        items.append(item)
                    relations[k] = items
        return {**data, **relations}

    @root_validator
    def cast_neo4j_datetime(cls, data: Dict) -> Dict:
        """Cast neo4j datetime to python datetime."""
        datetime_fields = {
            k: v.to_native()
            for k, v in data.items()
            if isinstance(v, DateTime)
        }
        return {**data, **datetime_fields}

    class Config:
        validate_assignment = True
        orm_mode = True


class BaseNodeQuery(BaseModel):
    """Base Model used to retrieve possible query parameters when performing
    nodes get operations with filters.

    Always validate assignments.
    """

    description: Optional[str] = None

    class Config:
        validate_assignment = True
