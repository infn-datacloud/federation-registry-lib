from typing import Any

from pytest_cases import parametrize_with_cases

from fed_reg.provider.schemas_extended import (
    ObjectStorageQuotaCreateExtended,
    ObjectStorageServiceCreateExtended,
)
from fed_reg.service.enum import ObjectStorageServiceName, ServiceType
from fed_reg.service.models import ObjectStorageService
from fed_reg.service.schemas import (
    ObjectStorageServiceBase,
    ObjectStorageServiceRead,
    ObjectStorageServiceReadPublic,
    ObjectStorageServiceUpdate,
)
from tests.create_dict import object_storage_service_schema_dict


@parametrize_with_cases("key, value", has_tag="base")
def test_base(key: str, value: Any) -> None:
    d = object_storage_service_schema_dict()
    if key:
        d[key] = value
    item = ObjectStorageServiceBase(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.type == ServiceType.OBJECT_STORAGE.value
    assert item.name == d.get("name").value


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(
    object_storage_service_model: ObjectStorageService, key: str, value: str
) -> None:
    if key:
        object_storage_service_model.__setattr__(key, value)
    item = ObjectStorageServiceReadPublic.from_orm(object_storage_service_model)

    assert item.uid
    assert item.uid == object_storage_service_model.uid
    assert item.description == object_storage_service_model.description
    assert item.endpoint == object_storage_service_model.endpoint


@parametrize_with_cases("key, value", has_tag="base")
def test_read(
    object_storage_service_model: ObjectStorageService, key: str, value: Any
) -> None:
    if key:
        if isinstance(value, ObjectStorageServiceName):
            value = value.value
        object_storage_service_model.__setattr__(key, value)
    item = ObjectStorageServiceRead.from_orm(object_storage_service_model)

    assert item.uid
    assert item.uid == object_storage_service_model.uid
    assert item.description == object_storage_service_model.description
    assert item.endpoint == object_storage_service_model.endpoint
    assert item.type == object_storage_service_model.type
    assert item.name == object_storage_service_model.name


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = object_storage_service_schema_dict()
    if key:
        d[key] = value
    item = ObjectStorageServiceUpdate(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.type == ServiceType.OBJECT_STORAGE.value
    assert item.name == (d.get("name").value if d.get("name") else None)


@parametrize_with_cases("quotas", has_tag="create_extended")
def test_create_extended(quotas: list[ObjectStorageQuotaCreateExtended]) -> None:
    d = object_storage_service_schema_dict()
    d["quotas"] = quotas
    item = ObjectStorageServiceCreateExtended(**d)
    assert item.quotas == quotas


# TODO Test read extended classes
