from typing import Union

import pytest
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize_with_cases

from app.quota.models import BlockStorageQuota, ComputeQuota, NetworkQuota
from tests.common.utils import random_lower_string


class CaseQuotaEmpty:
    def case_block_storage_quota(self) -> BlockStorageQuota:
        return BlockStorageQuota()

    def case_compute_quota(self) -> ComputeQuota:
        return ComputeQuota()

    def case_network_quota(self) -> NetworkQuota:
        return NetworkQuota()


def test_block_storage_default_attr() -> None:
    t = random_lower_string()
    item = BlockStorageQuota(type=t)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == t
    assert item.per_user is False
    assert item.gigabytes is None
    assert item.per_volume_gigabytes is None
    assert item.volumes is None
    assert isinstance(item.service, RelationshipManager)


def test_compute_default_attr() -> None:
    t = random_lower_string()
    item = ComputeQuota(type=t)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == t
    assert item.per_user is False
    assert item.cores is None
    assert item.instances is None
    assert item.ram is None
    assert isinstance(item.service, RelationshipManager)


def test_network_default_attr() -> None:
    t = random_lower_string()
    item = NetworkQuota(type=t)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == t
    assert item.per_user is False
    assert item.public_ips is None
    assert item.networks is None
    assert item.ports is None
    assert item.security_groups is None
    assert item.security_group_rules is None
    assert isinstance(item.service, RelationshipManager)


@parametrize_with_cases("item", cases=CaseQuotaEmpty)
def test_missing_attr(
    item: Union[BlockStorageQuota, ComputeQuota, NetworkQuota],
) -> None:
    with pytest.raises(RequiredProperty):
        item.save()
