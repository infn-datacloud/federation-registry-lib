from typing import Any
from uuid import uuid4

from pytest_cases import parametrize_with_cases

from fed_reg.provider.schemas_extended import BlockStorageQuotaCreateExtended
from fed_reg.quota.enum import QuotaType
from fed_reg.quota.models import BlockStorageQuota
from fed_reg.quota.schemas import (
    BlockStorageQuotaBase,
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    BlockStorageQuotaUpdate,
)


@parametrize_with_cases("key, value")
def test_base(key: str, value: Any) -> None:
    d = {key: value} if key else {}
    item = BlockStorageQuotaBase(**d)
    assert item.per_user == d.get("per_user", False)
    assert item.type == QuotaType.BLOCK_STORAGE.value
    assert item.gigabytes == d.get("gigabytes")
    assert item.per_volume_gigabytes == d.get("per_volume_gigabytes")
    assert item.volumes == d.get("volumes")


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = {key: value} if key else {}
    item = BlockStorageQuotaUpdate(**d)
    assert item.type == QuotaType.BLOCK_STORAGE.value


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(
    block_storage_quota_model: BlockStorageQuota, key: str, value: str
) -> None:
    if key:
        block_storage_quota_model.__setattr__(key, value)
    item = BlockStorageQuotaReadPublic.from_orm(block_storage_quota_model)

    assert item.uid
    assert item.uid == block_storage_quota_model.uid
    assert item.description == block_storage_quota_model.description
    assert item.per_user == block_storage_quota_model.per_user


@parametrize_with_cases("key, value")
def test_read(
    block_storage_quota_model: BlockStorageQuota, key: str, value: Any
) -> None:
    if key:
        block_storage_quota_model.__setattr__(key, value)
    item = BlockStorageQuotaRead.from_orm(block_storage_quota_model)

    assert item.uid
    assert item.uid == block_storage_quota_model.uid
    assert item.description == block_storage_quota_model.description
    assert item.per_user == block_storage_quota_model.per_user
    assert item.type == block_storage_quota_model.type
    assert item.gigabytes == block_storage_quota_model.gigabytes
    assert item.per_volume_gigabytes == block_storage_quota_model.per_volume_gigabytes
    assert item.volumes == block_storage_quota_model.volumes


def test_create_extended() -> None:
    d = {"project": uuid4()}
    item = BlockStorageQuotaCreateExtended(**d)
    assert item.project == d["project"].hex


# TODO Test read extended classes
