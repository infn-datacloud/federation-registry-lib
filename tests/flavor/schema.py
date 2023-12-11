"""Module to test Flavor schema creation."""
from datetime import date
from typing import Any, Dict, List, Union
from uuid import UUID, uuid4

from neomodel import One, OneOrMore, ZeroOrMore, ZeroOrOne
from pydantic.fields import SHAPE_LIST
from pytest_cases import parametrize

from app.flavor.models import Flavor
from app.flavor.schemas import (
    FlavorBase,
    FlavorBasePublic,
    FlavorRead,
    FlavorReadPublic,
)
from app.flavor.schemas_extended import FlavorReadExtended, FlavorReadExtendedPublic
from app.provider.schemas_extended import FlavorCreateExtended
from tests.utils.utils import random_lower_string

is_public = {True, False}
is_extended = {True, False}
invalid_key_values = {
    ("uuid", None),
    ("name", None),
    ("disk", -1),
    ("ram", -1),
    ("vcpus", -1),
    ("swap", -1),
    ("ephemeral", -1),
    ("gpu_model", random_lower_string()),  # gpus is 0
    ("gpu_vendor", random_lower_string()),  # gpus is 0
}
relationships_num = {0, 1, 2}


class ValidCreateData:
    """Valid data for create schemas."""

    @parametrize("is_public", is_public)
    def case_valid_data_default(
        self, is_public: bool, data_mandatory: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Valid set of Flavor mandatory attributes and relationships."""
        kwargs = {**data_mandatory}
        if not is_public:
            kwargs["is_public"] = is_public
            kwargs["projects"] = [uuid4()]
        return kwargs

    def case_valid_data(self, data_all: Dict[str, Any]) -> Dict[str, Any]:
        """Valid set of Flavor attributes and relationships."""
        kwargs = {**data_all}
        if not kwargs["is_public"]:
            kwargs["projects"] = [uuid4()]
        return kwargs


class InvalidCreateData:
    """Invalid data for create schemas."""

    @parametrize("k, v", invalid_key_values)
    def case_invalid_key_values(
        self, k: str, v: Any, data_mandatory: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Invalid set of Flavor attributes."""
        kwargs = {**data_mandatory}
        kwargs[k] = v
        return kwargs

    @parametrize("is_public", is_public)
    def case_invalid_projects_list_size(
        self, is_public: bool, data_mandatory: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Invalid project list size.

        Invalid cases: If flavor is marked as public, the list has at least one element,
        if private, the list has no items.
        """
        kwargs = {**data_mandatory}
        kwargs["is_public"] = is_public
        kwargs["projects"] = None if not is_public else [uuid4()]
        return kwargs

    def case_duplicated_projects(
        self, data_mandatory: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Invalid case: the project list has duplicate values."""
        project_uuid = uuid4()
        kwargs = {**data_mandatory}
        kwargs["is_public"] = False
        kwargs["projects"] = [project_uuid, project_uuid]
        return kwargs


class ReadSchemaVisibility:
    """Class for public/private cases."""

    @parametrize("public", is_public)
    def case_public_schema(self, public: bool) -> bool:
        """Return True if the schema is the public one."""
        return public


class ReadSchemaConnection:
    """Class for extended/short cases."""

    @parametrize("extended", is_extended)
    def case_extended_schema(self, extended: bool) -> bool:
        """Return True if the schema is the extended one."""
        return extended


class BaseSchemaValidation:
    """Class with functions used to validate Flavor schemas."""

    def validate_attrs(
        self, *, data: Dict[str, Any], schema: FlavorBase, public: bool = False
    ) -> None:
        """Validate data attributes with the expected ones.

        Args:
        ----
            data (dict): Dict with the original data.
            schema (FlavorCreateExtended): Schema with the info generated from data and
                to be validated.
            public (bool): Public or private schema.
        """
        attrs = FlavorBasePublic.__fields__ if public else FlavorBase.__fields__
        for attr, value in attrs.items():
            schema_attr = schema.__getattribute__(attr)
            if isinstance(schema_attr, date):
                schema_attr = schema_attr.isoformat()
            data_attr = data.pop(attr, value.default)
            if isinstance(data_attr, UUID):
                data_attr = data_attr.hex
            assert schema_attr == data_attr


class CreateSchemaValidation(BaseSchemaValidation):
    """Class with functions used to validate Flavor Create schemas."""

    def validate_create_ext_attrs(
        self, *, data: Dict[str, Any], schema: FlavorCreateExtended
    ) -> None:
        """Validate data attributes and relationships with the expected ones.

        Validate attributes and relationships.

        Args:
        ----
            data (dict): Dict with the original data.
            schema (FlavorCreateExtended): Schema with the info generated from data and
                to be validated.
        """
        self.validate_attrs(data=data, schema=schema, public=False)

        attrs = FlavorCreateExtended.__fields__.keys() - FlavorBase.__fields__.keys()
        for attr in attrs:
            field = FlavorCreateExtended.__fields__.get(attr)
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
                if isinstance(field.type_, str):
                    assert schema.__getattribute__(attr) == data.pop(attr).hex
                else:
                    pass
        assert not data


class ReadSchemaValidation(BaseSchemaValidation):
    """Class with functions used to validate Flavor Read schemas."""

    def validate_read_attrs(
        self,
        *,
        db_item: Flavor,
        schema: Union[
            FlavorRead, FlavorReadPublic, FlavorReadExtended, FlavorReadExtendedPublic
        ],
        public: bool,
        extended: bool,
    ) -> None:
        """Validate data attributes and relationships with the expected ones.

        Validate attributes and relationships.

        Args:
        ----
            db_item (Flavor): DB item with the data to read.
            schema (FlavorRead): Schema with the info generated from data and to be
                validated.
            public (bool): Public/shrunk schema.
            extended (bool): Schema with relationships.
        """
        data = db_item.__dict__

        if public:
            attrs = FlavorBase.__fields__.keys() - FlavorBasePublic.__fields__.keys()
            for attr in attrs:
                data.pop(attr)

        assert schema.uid == data.pop("uid")
        self.validate_attrs(data=data, schema=schema, public=public)

        if extended:
            attrs = FlavorReadExtended.__fields__.keys() - FlavorRead.__fields__.keys()
            for attr in attrs:
                value = data.pop(attr)

                if isinstance(value, (OneOrMore, ZeroOrMore)):
                    schema_list = schema.__getattribute__(attr)
                    assert len(schema_list) == len(value)

                    schema_list = sorted([x.uid for x in schema_list])
                    data_list = sorted([x.uid for x in value])
                    for schema_uid, data_uid in zip(schema_list, data_list):
                        assert schema_uid == data_uid
                else:
                    assert value.uid == value.uid
        else:
            to_remove = []
            for k, v in data.items():
                if isinstance(v, (One, OneOrMore, ZeroOrMore, ZeroOrOne)):
                    to_remove.append(k)
            for i in to_remove:
                data.pop(i)

        data.pop("id")
        assert not data
