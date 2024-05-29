from typing import Any

import pytest
from pytest_cases import parametrize_with_cases

from fed_reg.provider.schemas_extended import ComputeQuotaCreateExtended
from fed_reg.quota.models import ComputeQuota
from fed_reg.quota.schemas import ComputeQuotaBase, ComputeQuotaRead


@parametrize_with_cases("key, value")
def test_invalid_base(key: str, value: Any) -> None:
    d = {key: value}
    with pytest.raises(ValueError):
        ComputeQuotaBase(**d)


@parametrize_with_cases("key, value")
def test_invalid_read(compute_quota_model: ComputeQuota, key: str, value: str) -> None:
    compute_quota_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ComputeQuotaRead.from_orm(compute_quota_model)


def test_invalid_create_extended() -> None:
    d = {}
    with pytest.raises(ValueError):
        ComputeQuotaCreateExtended(**d)
