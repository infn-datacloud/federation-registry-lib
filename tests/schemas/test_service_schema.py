from typing import Any

import pytest
from pytest_cases import parametrize_with_cases

from fedreg.core import (
    BaseNodeCreate,
)
from fedreg.service.enum import ServiceType
from fedreg.service.schemas import (
    BlockStorageServiceCreate,
    BlockStorageServiceUpdate,
    ComputeServiceCreate,
    ComputeServiceUpdate,
    IdentityServiceCreate,
    IdentityServiceUpdate,
    NetworkServiceCreate,
    NetworkServiceUpdate,
    ObjectStoreServiceCreate,
    ObjectStoreServiceUpdate,
    ServiceBase,
)


def test_classes_inheritance() -> None:
    """Test pydantic schema inheritance."""
    # assert issubclass(ServiceBasePublic, BaseNode)

    # assert issubclass(ServiceBase, ServiceBasePublic)

    # assert issubclass(ServiceReadPublic, BaseNodeRead)
    # assert issubclass(ServiceReadPublic, BaseReadPublic)
    # assert issubclass(ServiceReadPublic, ServiceBasePublic)
    # assert ServiceReadPublic.__config__.orm_mode

    # assert issubclass(ServiceRead, BaseNodeRead)
    # assert issubclass(ServiceRead, BaseReadPrivate)
    # assert issubclass(ServiceRead, ServiceBase)
    # assert ServiceRead.__config__.orm_mode

    assert issubclass(BlockStorageServiceCreate, ServiceBase)
    assert issubclass(BlockStorageServiceCreate, BaseNodeCreate)
    assert issubclass(BlockStorageServiceUpdate, ServiceBase)
    assert issubclass(BlockStorageServiceUpdate, BaseNodeCreate)

    assert issubclass(ComputeServiceCreate, ServiceBase)
    assert issubclass(ComputeServiceCreate, BaseNodeCreate)
    assert issubclass(ComputeServiceUpdate, ServiceBase)
    assert issubclass(ComputeServiceUpdate, BaseNodeCreate)

    assert issubclass(IdentityServiceCreate, ServiceBase)
    assert issubclass(IdentityServiceCreate, BaseNodeCreate)
    assert issubclass(IdentityServiceUpdate, ServiceBase)
    assert issubclass(IdentityServiceUpdate, BaseNodeCreate)

    assert issubclass(NetworkServiceCreate, ServiceBase)
    assert issubclass(NetworkServiceCreate, BaseNodeCreate)
    assert issubclass(NetworkServiceUpdate, ServiceBase)
    assert issubclass(NetworkServiceUpdate, BaseNodeCreate)

    assert issubclass(ObjectStoreServiceCreate, ServiceBase)
    assert issubclass(ObjectStoreServiceCreate, BaseNodeCreate)
    assert issubclass(ObjectStoreServiceUpdate, ServiceBase)
    assert issubclass(ObjectStoreServiceUpdate, BaseNodeCreate)


# @parametrize_with_cases("data", has_tag=("dict", "valid", "base_public"))
# def test_base_public(data: dict[str, Any]) -> None:
#     """Test ServiceBasePublic class' mandatory and optional attributes."""
#     item = ServiceBasePublic(**data)
#     assert item.description == data.get("description", "")
#     assert item.endpoint == data.get("endpoint")


@parametrize_with_cases("data", has_tag=("dict", "valid", "base"))
def test_base(data: dict[str, Any]) -> None:
    """Test ServiceBase class' mandatory and optional attributes."""
    item = ServiceBase(**data)
    assert item.description == data.get("description", "")
    assert item.endpoint == data.get("endpoint")


@parametrize_with_cases("data", has_tag=("dict", "valid", "block-storage"))
def test_block_storage_create(data: dict[str, Any]) -> None:
    """Test BlockStorageServiceCreate class' mandatory and optional attributes."""
    item = BlockStorageServiceCreate(**data)
    assert item.description == data.get("description", "")
    assert item.endpoint == data.get("endpoint")
    assert item.name == data.get("name").value
    assert item.type == ServiceType.BLOCK_STORAGE.value


@parametrize_with_cases("data", has_tag=("dict", "valid", "compute"))
def test_compute_create(data: dict[str, Any]) -> None:
    """Test ComputeServiceCreate class' mandatory and optional attributes."""
    item = ComputeServiceCreate(**data)
    assert item.description == data.get("description", "")
    assert item.endpoint == data.get("endpoint")
    assert item.name == data.get("name").value
    assert item.type == ServiceType.COMPUTE.value


@parametrize_with_cases("data", has_tag=("dict", "valid", "identity"))
def test_identity_create(data: dict[str, Any]) -> None:
    """Test IdentityServiceCreate class' mandatory and optional attributes."""
    item = IdentityServiceCreate(**data)
    assert item.description == data.get("description", "")
    assert item.endpoint == data.get("endpoint")
    assert item.name == data.get("name").value
    assert item.type == ServiceType.IDENTITY.value


@parametrize_with_cases("data", has_tag=("dict", "valid", "network"))
def test_network_create(data: dict[str, Any]) -> None:
    """Test NetworkServiceCreate class' mandatory and optional attributes."""
    item = NetworkServiceCreate(**data)
    assert item.description == data.get("description", "")
    assert item.endpoint == data.get("endpoint")
    assert item.name == data.get("name").value
    assert item.type == ServiceType.NETWORK.value


@parametrize_with_cases("data", has_tag=("dict", "valid", "object-store"))
def test_object_store_create(data: dict[str, Any]) -> None:
    """Test ObjectStoreService class' mandatory and optional attributes."""
    item = ObjectStoreServiceCreate(**data)
    assert item.description == data.get("description", "")
    assert item.endpoint == data.get("endpoint")
    assert item.name == data.get("name").value
    assert item.type == ServiceType.OBJECT_STORE.value


@parametrize_with_cases("data", has_tag=("dict", "valid", "update", "block-storage"))
def test_block_storage_update(data: dict[str, Any]) -> None:
    """Test BlockStorageServiceUpdate class' attribute values."""
    item = BlockStorageServiceUpdate(**data)
    assert item.description == data.get("description", "")
    assert item.endpoint == data.get("endpoint", None)
    assert item.name == (data.get("name").value if data.get("name", None) else None)
    assert item.type == ServiceType.BLOCK_STORAGE.value


@parametrize_with_cases("data", has_tag=("dict", "valid", "update", "compute"))
def test_compute_update(data: dict[str, Any]) -> None:
    """Test ComputeServiceUpdate class' attribute values."""
    item = ComputeServiceUpdate(**data)
    assert item.description == data.get("description", "")
    assert item.endpoint == data.get("endpoint", None)
    assert item.name == (data.get("name").value if data.get("name", None) else None)
    assert item.type == ServiceType.COMPUTE.value


@parametrize_with_cases("data", has_tag=("dict", "valid", "update", "identity"))
def test_identity_update(data: dict[str, Any]) -> None:
    """Test IdentityServiceUpdate class' attribute values."""
    item = IdentityServiceUpdate(**data)
    assert item.description == data.get("description", "")
    assert item.endpoint == data.get("endpoint", None)
    assert item.name == (data.get("name").value if data.get("name", None) else None)
    assert item.type == ServiceType.IDENTITY.value


@parametrize_with_cases("data", has_tag=("dict", "valid", "update", "network"))
def test_network_update(data: dict[str, Any]) -> None:
    """Test NetworkServiceUpdate class' attribute values."""
    item = NetworkServiceUpdate(**data)
    assert item.description == data.get("description", "")
    assert item.endpoint == data.get("endpoint", None)
    assert item.name == (data.get("name").value if data.get("name", None) else None)
    assert item.type == ServiceType.NETWORK.value


@parametrize_with_cases("data", has_tag=("dict", "valid", "update", "object-store"))
def test_object_store_update(data: dict[str, Any]) -> None:
    """Test NetworkServiceUpdate class' attribute values."""
    item = ObjectStoreServiceUpdate(**data)
    assert item.description == data.get("description", "")
    assert item.endpoint == data.get("endpoint", None)
    assert item.name == (data.get("name").value if data.get("name", None) else None)
    assert item.type == ServiceType.OBJECT_STORE.value


# @parametrize_with_cases("data", has_tag=("dict", "valid"))
# def test_read_public(data: dict[str, Any]) -> None:
#     """Test ServiceReadPublic class' attribute values."""
#     uid = uuid4()
#     item = ServiceReadPublic(**data, uid=uid)
#     assert item.schema_type == "public"
#     assert item.uid == uid.hex
#     assert item.description == data.get("description", "")
#     assert item.endpoint == data.get("endpoint")
#     assert item.type == data.get("type", None)


# @parametrize_with_cases("data", has_tag=("dict", "valid"))
# def test_read(data: dict[str, Any]) -> None:
#     """Test ServiceRead class' attribute values."""
#     uid = uuid4()
#     item = ServiceRead(**data, uid=uid)
#     assert item.schema_type == "private"
#     assert item.uid == uid.hex
#     assert item.description == data.get("description", "")
#     assert item.endpoint == data.get("endpoint")
#     assert item.type == data.get("type", None)
#     assert item.name == data.get("name", None)


# @parametrize_with_cases("model", has_tag="model")
# def test_read_public_from_orm(
#     model: Service
#     | BlockStorageService
#     | ComputeService
#     | IdentityService
#     | NetworkService
#     | ObjectStoreService,
# ) -> None:
#     """Use the from_orm function of ServiceReadPublic to read data from an ORM."""
#     item = ServiceReadPublic.from_orm(model)
#     assert item.schema_type == "public"
#     assert item.uid == model.uid
#     assert item.description == model.description
#     assert item.endpoint == model.endpoint
#     if not isinstance(model, Service):
#         assert item.type == model.type


# @parametrize_with_cases("model", has_tag="model")
# def test_read_from_orm(
#     model: ServiceBase
#     | BlockStorageService
#     | ComputeService
#     | IdentityService
#     | NetworkService
#     | ObjectStoreService,
# ) -> None:
#     """Use the from_orm function of ServiceRead to read data from an ORM."""
#     item = ServiceRead.from_orm(model)
#     assert item.schema_type == "private"
#     assert item.uid == model.uid
#     assert item.description == model.description
#     assert item.endpoint == model.endpoint
#     if not isinstance(model, Service):
#         assert item.type == model.type
#         assert item.name == model.name


# @parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "base_public"))
# def test_invalid_base_public(data: dict[str, Any], attr: str) -> None:
#     """Test invalid attributes for ServiceBasePublic."""
#     err_msg = rf"1 validation error for ServiceBasePublic\s{attr}"
#     with pytest.raises(ValueError, match=err_msg):
#         ServiceBasePublic(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "base"))
def test_invalid_base(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for ServiceBase."""
    err_msg = rf"1 validation error for {ServiceBase.__name__}\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        ServiceBase(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "block-storage"))
def test_invalid_block_storage_create(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for BlockStorageServiceCreate."""
    err_msg = rf"1 validation error for {BlockStorageServiceCreate.__name__}\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        BlockStorageServiceCreate(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "compute"))
def test_invalid_compute_create(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for ComputeServiceCreate."""
    err_msg = rf"1 validation error for {ComputeServiceCreate.__name__}\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        ComputeServiceCreate(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "identity"))
def test_invalid_identity_create(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for IdentityServiceCreate."""
    err_msg = rf"1 validation error for {IdentityServiceCreate.__name__}\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        IdentityServiceCreate(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "network"))
def test_invalid_network_create(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for NetworkServiceCreate."""
    err_msg = rf"1 validation error for {NetworkServiceCreate.__name__}\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        NetworkServiceCreate(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "object-store"))
def test_invalid_object_store_create(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for ObjectStoreServiceCreate."""
    err_msg = rf"1 validation error for {ObjectStoreServiceCreate.__name__}\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        ObjectStoreServiceCreate(**data)


@parametrize_with_cases(
    "data, attr", has_tag=("dict", "invalid", "update", "block-storage")
)
def test_invalid_block_storage_update(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for BlockStorageServiceUpdate."""
    err_msg = rf"1 validation error for BlockStorageServiceUpdate\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        BlockStorageServiceUpdate(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "update", "compute"))
def test_invalid_compute_update(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for ComputeServiceUpdate."""
    err_msg = rf"1 validation error for ComputeServiceUpdate\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        ComputeServiceUpdate(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "update", "identity"))
def test_invalid_identity_update(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for IdentityServiceUpdate."""
    err_msg = rf"1 validation error for IdentityServiceUpdate\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        IdentityServiceUpdate(**data)


@parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "update", "network"))
def test_invalid_network_update(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for NetworkServiceUpdate."""
    err_msg = rf"1 validation error for NetworkServiceUpdate\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        NetworkServiceUpdate(**data)


@parametrize_with_cases(
    "data, attr", has_tag=("dict", "invalid", "update", "object-store")
)
def test_invalid_object_store_update(data: dict[str, Any], attr: str) -> None:
    """Test invalid attributes for ObjectStoreServiceUpdate."""
    err_msg = rf"1 validation error for ObjectStoreServiceUpdate\s{attr}"
    with pytest.raises(ValueError, match=err_msg):
        ObjectStoreServiceUpdate(**data)


# @parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "read_public"))
# def test_invalid_read_public(data: dict[str, Any], attr: str) -> None:
#     """Test invalid attributes for ServiceReadPublic."""
#     uid = uuid4()
#     err_msg = rf"1 validation error for ServiceReadPublic\s{attr}"
#     with pytest.raises(ValueError, match=err_msg):
#         ServiceReadPublic(**data, uid=uid)


# @parametrize_with_cases("data, attr", has_tag=("dict", "invalid", "read"))
# def test_invalid_read(data: dict[str, Any], attr: str) -> None:
#     """Test invalid attributes for ServiceRead."""
#     uid = uuid4()
#     if attr in ("name"):
#         err_msg = rf"validation errors for ServiceRead\s{attr}"
#     else:
#         err_msg = rf"1 validation error for ServiceRead\s{attr}"
#     with pytest.raises(ValueError, match=err_msg):
#         ServiceRead(**data, uid=uid)
