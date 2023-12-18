"""Module to test Flavor schema creation."""
from datetime import date
from enum import Enum
from typing import Any, Dict, Generic, Type, TypeVar
from uuid import UUID

from neomodel import StructuredNode
from pydantic.fields import SHAPE_LIST

from app.models import BaseNode, BaseNodeCreate, BaseNodeRead

BaseType = TypeVar("BaseType", bound=BaseNode)
BasePublicType = TypeVar("BasePublicType", bound=BaseNode)
CreateType = TypeVar("CreateType", bound=BaseNodeCreate)
DbType = TypeVar("DbType", bound=StructuredNode)
ReadType = TypeVar("ReadType", bound=BaseNodeRead)
ReadPublicType = TypeVar("ReadPublicType", bound=BaseNodeRead)
ReadExtendedType = TypeVar("ReadExtendedType", BaseNodeRead, None)
ReadExtendedPublicType = TypeVar("ReadExtendedPublicType", BaseNodeRead, None)


class BaseValidation(Generic[BaseType, BasePublicType]):
    """Class with functions used to validate Flavor schemas."""

    def __init__(
        self, *, base: Type[BaseType], base_public: Type[BasePublicType]
    ) -> None:
        """Define base and base public types.

        Args:
        ----
            base (type of BaseType): Schema class with public and private attributes.
            base_public (type of BasePublicType): Schema class with public attributes.
        """
        self.base = base
        self.base_public = base_public

    def validate_attrs(
        self, *, data: Dict[str, Any], schema: BaseType, public: bool = False
    ) -> None:
        """Validate data attributes with the expected ones.

        Args:
        ----
            data (dict): Dict with the original data.
            schema (CreateType): Schema with the info generated from data and
                to be validated.
            public (bool): Public or private schema.
        """
        attrs = self.base_public.__fields__ if public else self.base.__fields__
        for attr, value in attrs.items():
            schema_attr = schema.__getattribute__(attr)
            if isinstance(schema_attr, date):
                schema_attr = schema_attr.isoformat()
            if value.shape == SHAPE_LIST:
                default = value.default_factory()
            else:
                default = value.default
            data_attr = data.pop(attr, default)
            if isinstance(data_attr, UUID):
                data_attr = data_attr.hex
            elif isinstance(data_attr, Enum):
                data_attr = data_attr.value
            elif isinstance(data_attr, date):
                data_attr = data_attr.isoformat()
            assert schema_attr == data_attr
