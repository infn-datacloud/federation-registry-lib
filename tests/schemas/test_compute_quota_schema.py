from typing import Any
from uuid import uuid4

from pytest_cases import parametrize_with_cases

from fed_reg.provider.schemas_extended import ComputeQuotaCreateExtended
from fed_reg.quota.enum import QuotaType
from fed_reg.quota.models import ComputeQuota
from fed_reg.quota.schemas import (
    ComputeQuotaBase,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    ComputeQuotaUpdate,
)


@parametrize_with_cases("key, value")
def test_base(key: str, value: Any) -> None:
    d = {key: value} if key else {}
    item = ComputeQuotaBase(**d)
    assert item.per_user == d.get("per_user", False)
    assert item.type == QuotaType.COMPUTE.value
    assert item.cores == d.get("cores")
    assert item.instances == d.get("instances")
    assert item.ram == d.get("ram")


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(compute_quota_model: ComputeQuota, key: str, value: str) -> None:
    if key:
        compute_quota_model.__setattr__(key, value)
    item = ComputeQuotaReadPublic.from_orm(compute_quota_model)

    assert item.uid
    assert item.uid == compute_quota_model.uid
    assert item.description == compute_quota_model.description
    assert item.per_user == compute_quota_model.per_user


@parametrize_with_cases("key, value")
def test_read(compute_quota_model: ComputeQuota, key: str, value: Any) -> None:
    if key:
        compute_quota_model.__setattr__(key, value)
    item = ComputeQuotaRead.from_orm(compute_quota_model)

    assert item.uid
    assert item.uid == compute_quota_model.uid
    assert item.description == compute_quota_model.description
    assert item.per_user == compute_quota_model.per_user
    assert item.type == compute_quota_model.type
    assert item.cores == compute_quota_model.cores
    assert item.instances == compute_quota_model.instances
    assert item.ram == compute_quota_model.ram


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = {key: value} if key else {}
    item = ComputeQuotaUpdate(**d)
    assert item.type == QuotaType.COMPUTE.value


def test_create_extended() -> None:
    d = {"project": uuid4()}
    item = ComputeQuotaCreateExtended(**d)
    assert item.project == d["project"].hex


# TODO Test read extended classes
