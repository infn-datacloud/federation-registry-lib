from enum import Enum
from neo4j.data import DateTime
from neomodel import One, OneOrMore, ZeroOrOne, ZeroOrMore
from pydantic import UUID4, BaseModel, Extra, root_validator
from typing import Dict, Optional


class BaseNodeCreate(BaseModel):
    """Node Base Model when updating or creating data.
    Always validate assignments.

    Attributes:
        description (str): Brief description.
    """

    description: str = ""

    @root_validator
    def get_value_from_enums(cls, data: Dict) -> Dict:
        """Get value from all the enumeration field values."""
        enumeration_fields = {
            k: v.value for k, v in data.items() if isinstance(v, Enum)
        }
        return {**data, **enumeration_fields}

    class Config:
        validate_assignment = True
        extra = Extra.ignore


class BaseNodeRead(BaseModel):
    """Node Base Model when reading data.
    Use ORM mode to read data from DB models.

    Attributes:
        uid (UUID4): unique identifier.
        description (str): Brief description.
    """

    uid: UUID4
    description: str = ""

    @root_validator(pre=True)
    def get_relations(cls, data: Dict) -> Dict:
        """
        From One or ZeroOrOne relationships get that single relationship.
        From OneOrMore or ZeroOrMore relationships get all relationships;
        if that relationships has a model return a dict with the data stored
        in the relationship.
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
        extra = Extra.ignore
        orm_mode = True


class BaseNodeQuery(BaseModel):
    """Node Base Model used to retrieve possible
    query parameters when performing get operations
    with filters.
    Always validate assignments.

    Attributes:
        description (str): Brief description.
    """

    description: Optional[str] = None

    class Config:
        validate_assignment = True
        extra = Extra.ignore


class BaseProviderRelCreate(BaseModel):
    """Provider Relationship Base Model when updating or creating data.
    Always validate assignments.

    Attributes:
        uuid (UUID4): unique identifier of this item
            given by the provider.
        name (str): unique name of this item
            given by the provider.
    """

    name: str
    uuid: UUID4

    class Config:
        validate_assignment = True
        extra = Extra.ignore


class BaseProviderRelRead(BaseModel):
    """Provider Relationship Base Model when reading data.
    Use ORM mode to read data from DB models.

    Attributes:
        uuid (UUID4): unique identifier of this item
            given by the provider.
        name (str): unique name of this item
            given by the provider.
    """

    name: str
    uuid: UUID4

    class Config:
        validate_assignment = True
        extra = Extra.ignore
        orm_mode = True


class BaseProviderRelQuery(BaseModel):
    """Provider Relationship Base Model used to retrieve possible
    query parameters when performing get operations
    with filters.
    Always validate assignments.

    Attributes:
        uuid (UUID4 | None): unique identifier of this item
            given by the provider.
        name (str | None): unique name of this item
            given by the provider.
    """

    name: Optional[str] = None
    uuid: Optional[UUID4] = None

    class Config:
        validate_assignment = True
        extra = Extra.ignore
