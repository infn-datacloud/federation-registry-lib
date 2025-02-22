from typing import Any

import pytest
from pytest_cases import parametrize_with_cases

from fedreg.models import BaseNodeCreate
from fedreg.quota.enum import QuotaType
from fedreg.quota.schemas import (
    BlockStorageQuotaCreate,
    BlockStorageQuotaUpdate,
    ComputeQuotaCreate,
    ComputeQuotaUpdate,
    NetworkQuotaCreate,
    NetworkQuotaUpdate,
    ObjectStoreQuotaCreate,
    ObjectStoreQuotaUpdate,
    QuotaBase,
)


def test_classes_inheritance() -> None:
    """Test pydantic schema inheritance."""
    # assert issubclass(QuotaBasePublic, BaseNode)

    # assert issubclass(QuotaBase, QuotaBasePublic)

    # assert issubclass(QuotaReadPublic, BaseNodeRead)
    # assert issubclass(QuotaReadPublic, BaseReadPublic)
    # assert issubclass(QuotaReadPublic, QuotaBasePublic)
    # assert QuotaReadPublic.__config__.orm_mode

    # assert issubclass(QuotaRead, BaseNodeRead)
    # assert issubclass(QuotaRead, BaseReadPrivate)
    # assert issubclass(QuotaRead, QuotaBase)
    # assert QuotaRead.__config__.orm_mode

    assert issubclass(BlockStorageQuotaCreate, QuotaBase)
    assert issubclass(BlockStorageQuotaCreate, BaseNodeCreate)
    assert issubclass(BlockStorageQuotaUpdate, QuotaBase)
    assert issubclass(BlockStorageQuotaUpdate, BaseNodeCreate)

    assert issubclass(ComputeQuotaCreate, QuotaBase)
    assert issubclass(ComputeQuotaCreate, BaseNodeCreate)
    assert issubclass(ComputeQuotaUpdate, QuotaBase)
    assert issubclass(ComputeQuotaUpdate, BaseNodeCreate)

    assert issubclass(NetworkQuotaCreate, QuotaBase)
    assert issubclass(NetworkQuotaCreate, BaseNodeCreate)
    assert issubclass(NetworkQuotaUpdate, QuotaBase)
    assert issubclass(NetworkQuotaUpdate, BaseNodeCreate)

    assert issubclass(ObjectStoreQuotaCreate, QuotaBase)
    assert issubclass(ObjectStoreQuotaCreate, BaseNodeCreate)
    assert issubclass(ObjectStoreQuotaUpdate, QuotaBase)
    assert issubclass(ObjectStoreQuotaUpdate, BaseNodeCreate)


# @parametrize_with_cases("data", has_tag=("dict", "valid", "base_public"))
# def test_base_public(data: dict[str, Any]) -> None:
#     """Test QuotaBasePublic class' mandatory and optional attributes."""
#     item = QuotaBasePublic(**data)
#     assert item.description == data.get("description", "")
#     assert item.endpoint == data.get("endpoint")


@parametrize_with_cases("data", has_tag=("dict", "valid", "base"))
def test_base(data: dict[str, Any]) -> None:
    """Test QuotaBase class' mandatory and optional attributes."""
    item = QuotaBase(**data)
    assert item.description == data.get("description", "")
    assert item.per_user == data.get("per_user", False)
    assert item.usage == data.get("usage", False)


@parametrize_with_cases("data", has_tag=("dict", "valid", "block-storage"))
def test_block_storage_create(data: dict[str, Any]) -> None:
    """Test BlockStorageQuotaCreate class' mandatory and optional attributes."""
    item = BlockStorageQuotaCreate(**data)
    assert item.description == data.get("description", "")
    assert item.per_user == data.get("per_user", False)
    assert item.usage == data.get("usage", False)
    assert item.type == QuotaType.BLOCK_STORAGE.value
    assert item.gigabytes == data.get("gigabytes", None)
    assert item.per_volume_gigabytes == data.get("per_volume_gigabytes", None)
    assert item.volumes == data.get("volumes", None)


@parametrize_with_cases("data", has_tag=("dict", "valid", "compute"))
def test_compute_create(data: dict[str, Any]) -> None:
    """Test ComputeQuotaCreate class' mandatory and optional attributes."""
    item = ComputeQuotaCreate(**data)
    assert item.description == data.get("description", "")
    assert item.per_user == data.get("per_user", False)
    assert item.usage == data.get("usage", False)
    assert item.type == QuotaType.COMPUTE.value
    assert item.cores == data.get("cores", None)
    assert item.instances == data.get("instances", None)
    assert item.ram == data.get("ram", None)


@parametrize_with_cases("data", has_tag=("dict", "valid", "network"))
def test_network_create(data: dict[str, Any]) -> None:
    """Test NetworkQuotaCreate class' mandatory and optional attributes."""
    item = NetworkQuotaCreate(**data)
    assert item.description == data.get("description", "")
    assert item.per_user == data.get("per_user", False)
    assert item.usage == data.get("usage", False)
    assert item.type == QuotaType.NETWORK.value
    assert item.public_ips == data.get("public_ips", None)
    assert item.networks == data.get("networks", None)
    assert item.ports == data.get("ports", None)
    assert item.security_groups == data.get("security_groups", None)
    assert item.security_group_rules == data.get("security_group_rules", None)


@parametrize_with_cases("data", has_tag=("dict", "valid", "object-store"))
def test_object_store_create(data: dict[str, Any]) -> None:
    """Test ObjectStoreQuota class' mandatory and optional attributes."""
    item = ObjectStoreQuotaCreate(**data)
    assert item.description == data.get("description", "")
    assert item.per_user == data.get("per_user", False)
    assert item.usage == data.get("usage", False)
    assert item.type == QuotaType.OBJECT_STORE.value
    assert item.bytes == data.get("bytes", -1)
    assert item.containers == data.get("containers", 1000)
    assert item.objects == data.get("objects", -1)


@parametrize_with_cases("data", has_tag=("dict", "valid", "update", "block-storage"))
def test_block_storage_update(data: dict[str, Any]) -> None:
    """Test BlockStorageQuotaUpdate class' attribute values."""
    item = BlockStorageQuotaUpdate(**data)
    assert item.description == data.get("description", "")
    assert item.per_user == data.get("per_user", False)
    assert item.usage == data.get("usage", False)
    assert item.type == QuotaType.BLOCK_STORAGE.value
    assert item.gigabytes == data.get("gigabytes", None)
    assert item.per_volume_gigabytes == data.get("per_volume_gigabytes", None)
    assert item.volumes == data.get("volumes", None)


@parametrize_with_cases("data", has_tag=("dict", "valid", "update", "compute"))
def test_compute_update(data: dict[str, Any]) -> None:
    """Test ComputeQuotaUpdate class' attribute values."""
    item = ComputeQuotaUpdate(**data)
    assert item.description == data.get("description", "")
    assert item.per_user == data.get("per_user", False)
    assert item.usage == data.get("usage", False)
    assert item.type == QuotaType.COMPUTE.value
    assert item.cores == data.get("cores", None)
    assert item.instances == data.get("instances", None)
    assert item.ram == data.get("ram", None)


@parametrize_with_cases("data", has_tag=("dict", "valid", "update", "network"))
def test_network_update(data: dict[str, Any]) -> None:
    """Test NetworkQuotaUpdate class' attribute values."""
    item = NetworkQuotaUpdate(**data)
    assert item.description == data.get("description", "")
    assert item.per_user == data.get("per_user", False)
    assert item.usage == data.get("usage", False)
    assert item.type == QuotaType.NETWORK.value
    assert item.public_ips == data.get("public_ips", None)
    assert item.networks == data.get("networks", None)
    assert item.ports == data.get("ports", None)
    assert item.security_groups == data.get("security_groups", None)
    assert item.security_group_rules == data.get("security_group_rules", None)


@parametrize_with_cases("data", has_tag=("dict", "valid", "update", "object-store"))
def test_object_store_update(data: dict[str, Any]) -> None:
    """Test NetworkQuotaUpdate class' attribute values."""
    item = ObjectStoreQuotaUpdate(**data)
    assert item.description == data.get("description", "")
    assert item.per_user == data.get("per_user", False)
    assert item.usage == data.get("usage", False)
    assert item.type == QuotaType.OBJECT_STORE.value
    assert item.bytes == data.get("bytes", -1)
    assert item.containers == data.get("containers", 1000)
    assert item.objects == data.get("objects", -1)


# @parametrize_with_cases("data", has_tag=("dict", "valid"))
# def test_read_public(data: dict[str, Any]) -> None:
#     """Test QuotaReadPublic class' attribute values."""
#     uid = uuid4()
#     item = QuotaReadPublic(**data, uid=uid)
#     assert item.schema_type == "public"
#     assert item.uid == uid.hex
#     assert item.description == data.get("description", "")
#     assert item.endpoint == data.get("endpoint")
#     assert item.type == data.get("type", None)


# @parametrize_with_cases("data", has_tag=("dict", "valid"))
# def test_read(data: dict[str, Any]) -> None:
#     """Test QuotaRead class' attribute values."""
#     uid = uuid4()
#     item = QuotaRead(**data, uid=uid)
#     assert item.schema_type == "private"
#     assert item.uid == uid.hex
#     assert item.description == data.get("description", "")
#     assert item.endpoint == data.get("endpoint")
#     assert item.type == data.get("type", None)
#     assert item.name == data.get("name", None)


# @parametrize_with_cases("model", has_tag="model")
# def test_read_public_from_orm(
#     model: Quota
#     | BlockStorageQuota
#     | ComputeQuota
#     | IdentityQuota
#     | NetworkQuota
#     | ObjectStoreQuota,
# ) -> None:
#     """Use the from_orm function of QuotaReadPublic to read data from an ORM."""
#     item = QuotaReadPublic.from_orm(model)
#     assert item.schema_type == "public"
#     assert item.uid == model.uid
#     assert item.description == model.description
#     assert item.endpoint == model.endpoint
#     if not isinstance(model, Quota):
#         assert item.type == model.type


# @parametrize_with_cases("model", has_tag="model")
# def test_read_from_orm(
#     model: QuotaBase
#     | BlockStorageQuota
#     | ComputeQuota
#     | IdentityQuota
#     | NetworkQuota
#     | ObjectStoreQuota,
# ) -> None:
#     """Use the from_orm function of QuotaRead to read data from an ORM."""
#     item = QuotaRead.from_orm(model)
#     assert item.schema_type == "private"
#     assert item.uid == model.uid
#     assert item.description == model.description
#     assert item.endpoint == model.endpoint
#     if not isinstance(model, Quota):
#         assert item.type == model.type
#         assert item.name == model.name


# @parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "base_public"))
# def test_invalid_base_public(data: dict[str, Any], attr: str) -> None:
#     """Test invalid attributes for QuotaBasePublic."""
#     err_msg = rf"1 validation error for QuotaBasePublic\s{attr}"
#     with pytest.raises(ValueError, match=err_msg):
#         QuotaBasePublic(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "base"))
def test_invalid_base(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for QuotaBase."""
    err_msg = rf"1 validation error for {QuotaBase.__name__}\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        QuotaBase(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "block-storage"))
def test_invalid_block_storage_create(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for BlockStorageQuotaCreate."""
    err_msg = rf"1 validation error for {BlockStorageQuotaCreate.__name__}\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        BlockStorageQuotaCreate(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "compute"))
def test_invalid_compute_create(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for ComputeQuotaCreate."""
    err_msg = rf"1 validation error for {ComputeQuotaCreate.__name__}\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        ComputeQuotaCreate(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "network"))
def test_invalid_network_create(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for NetworkQuotaCreate."""
    err_msg = rf"1 validation error for {NetworkQuotaCreate.__name__}\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        NetworkQuotaCreate(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "object-store"))
def test_invalid_object_store_create(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for ObjectStoreQuotaCreate."""
    err_msg = rf"1 validation error for {ObjectStoreQuotaCreate.__name__}\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        ObjectStoreQuotaCreate(**data)


@parametrize_with_cases(
    "data, attr", has_tag=("dict", "invalid", "update", "block-storage")
)
def test_invalid_block_storage_update(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for BlockStorageQuotaUpdate."""
    err_msg = rf"1 validation error for BlockStorageQuotaUpdate\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        BlockStorageQuotaUpdate(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "update", "compute"))
def test_invalid_compute_update(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for ComputeQuotaUpdate."""
    err_msg = rf"1 validation error for ComputeQuotaUpdate\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        ComputeQuotaUpdate(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "update", "network"))
def test_invalid_network_update(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for NetworkQuotaUpdate."""
    err_msg = rf"1 validation error for NetworkQuotaUpdate\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        NetworkQuotaUpdate(**data)


@parametrize_with_cases(
    "data, attr", has_tag=("dict", "invalid", "update", "object-store")
)
def test_invalid_object_store_update(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for ObjectStoreQuotaUpdate."""
    err_msg = rf"1 validation error for ObjectStoreQuotaUpdate\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        ObjectStoreQuotaUpdate(**data)


# @parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "read_public"))
# def test_invalid_read_public(data: dict[str, Any], attr: str) -> None:
#     """Test invalid attributes for QuotaReadPublic."""
#     uid = uuid4()
#     err_msg = rf"1 validation error for QuotaReadPublic\s{attr}"
#     with pytest.raises(ValueError, match=err_msg):
#         QuotaReadPublic(**data, uid=uid)


# @parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "read"))
# def test_invalid_read(data: dict[str, Any], attr: str) -> None:
#     """Test invalid attributes for QuotaRead."""
#     uid = uuid4()
#     if attr in ("name"):
#         err_msg = rf"validation errors for QuotaRead\s{attr}"
#     else:
#         err_msg = rf"1 validation error for QuotaRead\s{attr}"
#     with pytest.raises(ValueError, match=err_msg):
#         QuotaRead(**data, uid=uid)
