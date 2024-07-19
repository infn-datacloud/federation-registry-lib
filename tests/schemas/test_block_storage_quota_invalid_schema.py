from typing import Any

import pytest
from pytest_cases import parametrize_with_cases

from fed_reg.provider.schemas_extended import BlockStorageQuotaCreateExtended
from fed_reg.quota.models import BlockStorageQuota
from fed_reg.quota.schemas import BlockStorageQuotaBase, BlockStorageQuotaRead


@parametrize_with_cases("key, value")
def test_invalid_base(key: str, value: Any) -> None:
    d = {key: value}
    with pytest.raises(ValueError):
        BlockStorageQuotaBase(**d)


@parametrize_with_cases("key, value")
def test_invalid_read(
    block_storage_quota_model: BlockStorageQuota, key: str, value: str
) -> None:
    block_storage_quota_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        BlockStorageQuotaRead.from_orm(block_storage_quota_model)


def test_invalid_create_extended() -> None:
    d = {}
    with pytest.raises(ValueError):
        BlockStorageQuotaCreateExtended(**d)
