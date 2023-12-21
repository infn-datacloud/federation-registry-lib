"""Module to test Flavor schema creation."""
from typing import Any, Dict, Generic, List, Optional, Type, Union
from uuid import UUID

from neomodel import One, OneOrMore, ZeroOrMore, ZeroOrOne
from pydantic.fields import SHAPE_LIST

from tests.common.validators import (
    BasePublicType,
    BaseType,
    BaseValidation,
    CreateType,
    DbType,
    ReadExtendedPublicType,
    ReadExtendedType,
    ReadPublicType,
    ReadType,
)


class CreateSchemaValidation(
    BaseValidation, Generic[BaseType, BasePublicType, CreateType]
):
    """Class with functions used to validate Create schemas."""

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
                    # We do not check this part since nested items checks are duplicates
                    # of other specific tests. We only pop the item if present.
                    data.pop(attr, None)
        assert not data


class PatchSchemaValidation(BaseValidation, Generic[BaseType, BasePublicType]):
    """Class with functions used to validate Update schemas."""


class ReadSchemaValidation(
    BaseValidation,
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
    """Class with functions used to validate Read schemas."""

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

    def _exclude_not_used_attrs(
        self, *, data: Dict[str, Any], exclude_attrs: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Do not consider not used attributes.

        Args:
        ----
            data (dict): Dict to filter.
            exclude_attrs (list of str): List of attributes marked as useless.

        Returns:
        -------
            The original data object without the attributes in exclude_attrs.
        """
        if exclude_attrs is None:
            exclude_attrs = []
        exclude_attrs.append("id")
        for i in exclude_attrs:
            data.pop(i, None)
        return data

    def _remove_relationships(self, *, data: Dict[str, Any]) -> Dict[str, Any]:
        """Do not consider relationships.

        Args:
        ----
            data (dict): Dict to filter.

        Returns:
        -------
            The original data object without the attributes corresponding to
            relationships.
        """
        to_remove = []
        for k, v in data.items():
            if isinstance(v, (One, OneOrMore, ZeroOrMore, ZeroOrOne)):
                to_remove.append(k)
        for i in to_remove:
            data.pop(i)
        return data

    def _validate_read_extended_attrs(
        self,
        *,
        data: Dict[str, Any],
        schema: Union[ReadExtendedType, ReadExtendedPublicType],
    ) -> Dict[str, Any]:
        """Check relationship consistency.

        With Zero to Many or One to Many relationships evaluate the list of UIDs. List
        can be empty.

        With One or Zero to One relationships evaluate the item's UID. Item can be None.

        Args:
        ----
            data (dict): Db object dictionary.
            schema (ReadExtendedType | ReadExtendedPublicType): Schema with the data to
                evaluate.

        Returns:
        -------
            The original data object without the attributes corresponding to
            relationships.
        """
        attrs = self.read_extended.__fields__.keys() - self.read.__fields__.keys()

        for attr in attrs:
            data_value = data.pop(attr)
            schema_value = schema.__getattribute__(attr)

            if isinstance(data_value, (list, OneOrMore, ZeroOrMore)):
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

        return data

    def validate_read_attrs(
        self,
        *,
        db_item: DbType,
        schema: Union[
            ReadType, ReadPublicType, ReadExtendedType, ReadExtendedPublicType
        ],
        public: bool,
        extended: bool,
        exclude_attrs: Optional[List[str]] = None,
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
            exclude_attrs (list of str): List of attributes of the database model to
                ignore.
        """
        data = db_item.__dict__

        if public:
            attrs = self.base.__fields__.keys() - self.base_public.__fields__.keys()
            for attr in attrs:
                data.pop(attr)

        assert schema.uid == data.pop("uid")
        self.validate_attrs(data=data, schema=schema, public=public)

        if extended:
            data = self._validate_read_extended_attrs(data=data, schema=schema)
        else:
            data = self._remove_relationships(data=data)

        data = self._exclude_not_used_attrs(data=data, exclude_attrs=exclude_attrs)
        assert not data
