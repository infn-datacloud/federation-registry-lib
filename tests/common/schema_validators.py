"""Module to test Flavor schema creation."""
from datetime import date
from typing import Any, Dict, Generic, List, Type, TypeVar, Union
from uuid import UUID

from neomodel import One, OneOrMore, StructuredNode, ZeroOrMore, ZeroOrOne
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


class BaseSchemaValidation(Generic[BaseType, BasePublicType]):
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
            assert schema_attr == data_attr


class CreateSchemaValidation(
    BaseSchemaValidation, Generic[BaseType, BasePublicType, CreateType]
):
    """Class with functions used to validate Flavor Create schemas."""

    def __init__(
        self,
        *,
        base: Type[BaseType],
        base_public: Type[BasePublicType],
        create: Type[CreateType],
    ) -> None:
        """Define base, base public and create types.

        Args:
        ----
            base (type of BaseType): Schema class with public and private attributes.
            base_public (type of BasePublicType): Schema class with public attributes.
            create (type of CreateType): Schema class to create an instance.
        """
        super().__init__(base=base, base_public=base_public)
        self.create = create

    def validate_create_ext_attrs(
        self, *, data: Dict[str, Any], schema: CreateType
    ) -> None:
        """Validate data attributes and relationships with the expected ones.

        Validate attributes and relationships.

        Args:
        ----
            data (dict): Dict with the original data.
            schema (CreateType): Schema with the info generated from data and
                to be validated.
        """
        self.validate_attrs(data=data, schema=schema, public=False)

        attrs = self.create.__fields__.keys() - self.base.__fields__.keys()
        for attr in attrs:
            field = self.create.__fields__.get(attr)
            if field.shape == SHAPE_LIST:
                schema_list = schema.__getattribute__(attr)
                data_list = data.pop(attr, [])
                assert len(schema_list) == len(data_list)

                if isinstance(field.type_, str):
                    schema_list = sorted([x.uuid for x in schema_list])
                    data_list: List[UUID] = sorted(data_list)
                    for schema_str, data_str in zip(schema_list, data_list):
                        assert schema_str == data_str.hex
                else:
                    pass
            else:
                if issubclass(field.type_, str):
                    v: UUID = data.pop(attr, None)
                    v = v.hex if v else v
                    assert schema.__getattribute__(attr) == v
                else:
                    pass
        assert not data


class ReadSchemaValidation(
    BaseSchemaValidation,
    Generic[
        BaseType,
        BasePublicType,
        ReadType,
        ReadPublicType,
        ReadExtendedType,
        ReadExtendedPublicType,
        DbType,
    ],
):
    """Class with functions used to validate Flavor Read schemas."""

    def __init__(
        self,
        *,
        base: Type[BaseType],
        base_public: Type[BasePublicType],
        read: Type[ReadType],
        read_extended: Type[ReadExtendedType],
    ) -> None:
        """Define base, base public, read, and read extended types.

        Args:
        ----
            base (type of BaseType): Schema class with public and private attributes.
            base_public (type of BasePublicType): Schema class with public attributes.
            read (type of ReadType): Schema class to read a db instance.
            read_extended (type of ReadExtendedType): Schema class to read a db instance
                with relationships.
        """
        super().__init__(base=base, base_public=base_public)
        self.read = read
        self.read_extended = read_extended

    def validate_read_attrs(
        self,
        *,
        db_item: DbType,
        schema: Union[
            ReadType, ReadPublicType, ReadExtendedType, ReadExtendedPublicType
        ],
        public: bool,
        extended: bool,
    ) -> None:
        """Validate data attributes and relationships with the expected ones.

        Validate attributes and relationships.

        Args:
        ----
            db_item (DbType): DB item with the data to read.
            schema (ReadType): Schema with the info generated from data and to be
                validated.
            public (bool): Public/shrunk schema.
            extended (bool): Schema with relationships.
        """
        data = db_item.__dict__

        if public:
            attrs = self.base.__fields__.keys() - self.base_public.__fields__.keys()
            for attr in attrs:
                data.pop(attr)

        assert schema.uid == data.pop("uid")
        self.validate_attrs(data=data, schema=schema, public=public)

        if extended:
            attrs = self.read_extended.__fields__.keys() - self.read.__fields__.keys()
            for attr in attrs:
                data_value = data.pop(attr)
                schema_value = schema.__getattribute__(attr)

                if isinstance(data_value, (OneOrMore, ZeroOrMore)):
                    assert len(schema_value) == len(data_value)

                    schema_list = sorted([x.uid for x in schema_value])
                    data_list = sorted([x.uid for x in data_value])
                    for schema_uid, data_uid in zip(schema_list, data_list):
                        assert schema_uid == data_uid
                else:
                    data_value = data_value.single()
                    data_uid = data_value.uid if data_value else data_value
                    schema_uid = schema_value.uid if schema_value else schema_value
                    assert schema_uid == data_uid
        else:
            to_remove = []
            for k, v in data.items():
                if isinstance(v, (One, OneOrMore, ZeroOrMore, ZeroOrOne)):
                    to_remove.append(k)
            for i in to_remove:
                data.pop(i)

        data.pop("id")
        assert not data
