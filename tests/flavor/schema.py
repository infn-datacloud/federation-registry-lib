"""Module to test Flavor schema creation."""
from datetime import date
from typing import Any, Dict, List
from uuid import UUID, uuid4

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
from tests.flavor.core import Core
from tests.utils.utils import random_lower_string

is_public = {True, False}
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
read_schema_types = {
    FlavorRead,
    FlavorReadPublic,
    FlavorReadExtended,
    FlavorReadExtendedPublic,
}


class ValidData(Core):
    """Valid data for create schemas."""

    @parametrize("is_public", is_public)
    def case_valid_data(self, is_public: bool) -> Dict[str, Any]:
        """Valid set of Flavor attributes and relationships."""
        kwargs = {**self.all_kwargs}
        kwargs["is_public"] = is_public
        if not is_public:
            kwargs["projects"] = [uuid4()]
        return kwargs

    @parametrize("is_public", is_public)
    def case_valid_data_default(self, is_public: bool) -> Dict[str, Any]:
        """Valid set of Flavor mandatory attributes and relationships."""
        kwargs = {**self.mandatory_kwargs}
        if not is_public:
            kwargs["is_public"] = is_public
            kwargs["projects"] = [uuid4()]
        return kwargs


class InvalidData(Core):
    """Invalid data for create schemas."""

    @parametrize("k, v", invalid_key_values)
    def case_invalid_key_values(self, k: str, v: Any) -> Dict[str, Any]:
        """Invalid set of Flavor attributes."""
        kwargs = {**self.mandatory_kwargs}
        kwargs[k] = v
        return kwargs

    @parametrize("is_public", is_public)
    def case_invalid_projects_list_size(self, is_public: bool) -> Dict[str, Any]:
        """Invalid project list size.

        Invalid cases: If flavor is marked as public, the list has at least one element,
        if private, the list has no items.
        """
        kwargs = {**self.mandatory_kwargs}
        kwargs["is_public"] = is_public
        kwargs["projects"] = None if not is_public else [uuid4()]
        return kwargs

    def case_duplicated_projects(self) -> Dict[str, Any]:
        """Invalid case: the project list has duplicate values."""
        project_uuid = uuid4()
        kwargs = {**self.mandatory_kwargs}
        kwargs["is_public"] = False
        kwargs["projects"] = [project_uuid, project_uuid]
        return kwargs


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
                schema_list: List[Flavor] = schema.__getattribute__(attr)
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


# class ReadSchema:
#     @parametrize("schema_type", read_schema_types)
#     def case_read_schema(self, schema_type: Type[BaseNodeRead]) -> Type[BaseNodeRead]:
#         return schema_type
