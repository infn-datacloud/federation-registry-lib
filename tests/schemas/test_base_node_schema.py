"""Test custom  authentication functions."""

from enum import Enum
from uuid import uuid4

import pytest
from pydantic import Field

from fedreg.core import BaseNode, BaseNodeCreate
from tests.utils import random_lower_string


class TestEnum(Enum):
    __test__ = False
    VALUE_1 = "value_1"
    VALUE_2 = "value_2"


class TestModelEnum(BaseNode):
    __test__ = False
    test_field: TestEnum = Field(description="A test field")


class TestModelNoDefault(BaseNode):
    __test__ = False
    test_field: str | None = Field(description="A test field")


class TestModelUUID(BaseNode):
    __test__ = False
    uuid: str = Field(default="", description="A test field for uuid")
    uuid_list: list[str] = Field(
        default_factory=list, description="A test field for list of uuids"
    )


class TestModelCreate(BaseNodeCreate):
    __test__ = False


def test_default() -> None:
    """Test the default description."""
    base_node = BaseNode()
    assert base_node.description is not None
    assert base_node.description == ""


def test_valid_schema() -> None:
    """Test a valid description."""
    desc = random_lower_string()
    base_node = BaseNode(description=desc)
    assert base_node.description is not None
    assert base_node.description == desc


def test_not_none() -> None:
    """Verify that if the value None is given, the default value is returned."""
    base_node = BaseNode(description=None)
    assert base_node.description is not None
    assert base_node.description == ""


def test_none() -> None:
    """Return None if there is no default value."""
    base_node = TestModelNoDefault(test_field=None)
    assert base_node.test_field is None

    base_node = TestModelNoDefault(test_field=None)
    assert base_node.test_field is None


def test_get_str_from_uuid() -> None:
    """Test the conversion of UUIDs to str."""
    uuid1 = uuid4()
    uuid2 = uuid4()
    uuid1_str = uuid1.hex
    uuid2_str = uuid2.hex
    s = random_lower_string()

    # Test with a single uuid
    item = TestModelUUID(uuid=uuid1)
    assert item.uuid == uuid1_str

    # Test with a list of uuids
    item = TestModelUUID(uuid_list=[uuid1, uuid2])
    assert item.uuid_list == [uuid1_str, uuid2_str]

    # Test with a single non-uuid value
    item = TestModelUUID(uuid=s)
    assert item.uuid == s

    # Test with a list of mixed uuid and non-uuid values
    item = TestModelUUID(uuid_list=[uuid1, s, uuid2])
    assert item.uuid_list == [uuid1_str, s, uuid2_str]


def test_get_value_from_enums() -> None:
    model_instance = TestModelEnum(test_field=TestEnum.VALUE_1)
    assert model_instance.test_field == TestEnum.VALUE_1.value

    with pytest.raises(ValueError):
        TestModelEnum(test_field="VALUE_2")


def test_base_node_create() -> None:
    """Test the BaseNodeCreate class."""
    test_model = TestModelCreate()
    assert test_model.__config__.validate_assignment is True
