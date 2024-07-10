from typing import Any

import pytest
from pytest_cases import parametrize_with_cases

from fed_reg.provider.schemas_extended import ObjectStoreQuotaCreateExtended
from fed_reg.quota.models import ObjectStoreQuota
from fed_reg.quota.schemas import ObjectStoreQuotaBase, ObjectStoreQuotaRead


@parametrize_with_cases("key, value")
def test_invalid_base(key: str, value: Any) -> None:
    d = {key: value}
    with pytest.raises(ValueError):
        ObjectStoreQuotaBase(**d)


@parametrize_with_cases("key, value")
def test_invalid_read(
    object_store_quota_model: ObjectStoreQuota, key: str, value: str
) -> None:
    object_store_quota_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ObjectStoreQuotaRead.from_orm(object_store_quota_model)


def test_invalid_create_extended() -> None:
    d = {}
    with pytest.raises(ValueError):
        ObjectStoreQuotaCreateExtended(**d)
