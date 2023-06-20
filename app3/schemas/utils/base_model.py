from enum import Enum
from typing import Dict, Optional
from pydantic import UUID4, BaseModel, root_validator
from neo4j.data import DateTime


class BaseNodeCreate(BaseModel):
    """Node Base Model when updating or creating data.
    Always validate assignments.

    Attributes:
        description (str): Brief description.
    """

    description: str = ""

    class Config:
        validate_assignment = True

    @root_validator()
    def get_value_from_enums(cls, data: Dict) -> Dict:
        """Get value from all the enumeration field values."""
        enumeration_fields = {
            k: v.value for k, v in data.items() if isinstance(v, Enum)
        }
        return {**data, **enumeration_fields}


class BaseNodeRead(BaseModel):
    """Node Base Model when reading data.
    Use ORM mode to read data from DB models.

    Attributes:
        uid (UUID): unique identifier.
        description (str): Brief description.
    """

    uid: UUID4
    description: str = ""

    class Config:
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

    @root_validator()
    def cast_neo4j_datetime(cls, data: Dict) -> Dict:
        """Get value from all the enumeration field values."""
        datetime_fields = {
            k: v.to_native() for k, v in data.items() if isinstance(v, DateTime)
        }
        return {**data, **datetime_fields}

    class Config:
        validate_assignment = True
