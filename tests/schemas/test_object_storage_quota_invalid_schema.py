from typing import Any

import pytest
from pytest_cases import parametrize_with_cases

from fed_reg.provider.schemas_extended import ObjectStorageQuotaCreateExtended
from fed_reg.quota.models import ObjectStorageQuota
from fed_reg.quota.schemas import ObjectStorageQuotaBase, ObjectStorageQuotaRead


@parametrize_with_cases("key, value")
def test_invalid_base(key: str, value: Any) -> None:
    d = {key: value}
    with pytest.raises(ValueError):
        ObjectStorageQuotaBase(**d)


@parametrize_with_cases("key, value")
def test_invalid_read(
    object_storage_quota_model: ObjectStorageQuota, key: str, value: str
) -> None:
    object_storage_quota_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ObjectStorageQuotaRead.from_orm(object_storage_quota_model)


def test_invalid_create_extended() -> None:
    d = {}
    with pytest.raises(ValueError):
        ObjectStorageQuotaCreateExtended(**d)
