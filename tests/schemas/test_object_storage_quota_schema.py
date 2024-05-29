from typing import Any
from uuid import uuid4

from pytest_cases import parametrize_with_cases

from fed_reg.provider.schemas_extended import ObjectStorageQuotaCreateExtended
from fed_reg.quota.enum import QuotaType
from fed_reg.quota.models import ObjectStorageQuota
from fed_reg.quota.schemas import (
    ObjectStorageQuotaBase,
    ObjectStorageQuotaRead,
    ObjectStorageQuotaReadPublic,
    ObjectStorageQuotaUpdate,
)


@parametrize_with_cases("key, value")
def test_base(key: str, value: Any) -> None:
    d = {key: value} if key else {}
    item = ObjectStorageQuotaBase(**d)
    assert item.per_user == d.get("per_user", False)
    assert item.type == QuotaType.OBJECT_STORAGE.value
    # TODO: understand attributes


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(
    object_storage_quota_model: ObjectStorageQuota, key: str, value: str
) -> None:
    if key:
        object_storage_quota_model.__setattr__(key, value)
    item = ObjectStorageQuotaReadPublic.from_orm(object_storage_quota_model)

    assert item.uid
    assert item.uid == object_storage_quota_model.uid
    assert item.description == object_storage_quota_model.description
    assert item.per_user == object_storage_quota_model.per_user


@parametrize_with_cases("key, value")
def test_read(
    object_storage_quota_model: ObjectStorageQuota, key: str, value: Any
) -> None:
    if key:
        object_storage_quota_model.__setattr__(key, value)
    item = ObjectStorageQuotaRead.from_orm(object_storage_quota_model)

    assert item.uid
    assert item.uid == object_storage_quota_model.uid
    assert item.description == object_storage_quota_model.description
    assert item.per_user == object_storage_quota_model.per_user
    assert item.type == object_storage_quota_model.type
    # TODO: Understand attributes


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = {key: value} if key else {}
    item = ObjectStorageQuotaUpdate(**d)
    assert item.type == QuotaType.OBJECT_STORAGE.value


def test_create_extended() -> None:
    d = {"project": uuid4()}
    item = ObjectStorageQuotaCreateExtended(**d)
    assert item.project == d["project"].hex


# TODO Test read extended classes
