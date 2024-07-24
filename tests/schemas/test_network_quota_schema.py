from typing import Any
from uuid import uuid4

from pytest_cases import parametrize_with_cases

from fed_reg.provider.schemas_extended import NetworkQuotaCreateExtended
from fed_reg.quota.enum import QuotaType
from fed_reg.quota.models import NetworkQuota
from fed_reg.quota.schemas import (
    NetworkQuotaBase,
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
    NetworkQuotaUpdate,
)


@parametrize_with_cases("key, value")
def test_base(key: str, value: Any) -> None:
    d = {key: value} if key else {}
    item = NetworkQuotaBase(**d)
    assert item.per_user == d.get("per_user", False)
    assert item.type == QuotaType.NETWORK.value
    assert item.public_ips == d.get("public_ips")
    assert item.networks == d.get("networks")
    assert item.ports == d.get("ports")
    assert item.security_groups == d.get("security_groups")
    assert item.security_group_rules == d.get("security_group_rules")


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(network_quota_model: NetworkQuota, key: str, value: str) -> None:
    if key:
        network_quota_model.__setattr__(key, value)
    item = NetworkQuotaReadPublic.from_orm(network_quota_model)

    assert item.uid
    assert item.uid == network_quota_model.uid
    assert item.description == network_quota_model.description
    assert item.per_user == network_quota_model.per_user


@parametrize_with_cases("key, value")
def test_read(network_quota_model: NetworkQuota, key: str, value: Any) -> None:
    if key:
        network_quota_model.__setattr__(key, value)
    item = NetworkQuotaRead.from_orm(network_quota_model)

    assert item.uid
    assert item.uid == network_quota_model.uid
    assert item.description == network_quota_model.description
    assert item.per_user == network_quota_model.per_user
    assert item.type == network_quota_model.type
    assert item.networks == network_quota_model.networks
    assert item.ports == network_quota_model.ports
    assert item.public_ips == network_quota_model.public_ips
    assert item.security_groups == network_quota_model.security_groups
    assert item.security_group_rules == network_quota_model.security_group_rules


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = {key: value} if key else {}
    item = NetworkQuotaUpdate(**d)
    assert item.type == QuotaType.NETWORK.value


def test_create_extended() -> None:
    d = {"project": uuid4()}
    item = NetworkQuotaCreateExtended(**d)
    assert item.project == d["project"].hex


# TODO Test read extended classes
