from random import randint
from typing import Any, Tuple, Union
from unittest.mock import Mock, PropertyMock, patch
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.quota.models import BlockStorageQuota, ComputeQuota, NetworkQuota
from tests.utils import random_lower_string


class CaseQuotaEmpty:
    def case_block_storage_quota(self) -> BlockStorageQuota:
        return BlockStorageQuota()

    def case_compute_quota(self) -> ComputeQuota:
        return ComputeQuota()

    def case_network_quota(self) -> NetworkQuota:
        return NetworkQuota()


class CaseBlockStorageAttr:
    @parametrize(key=["gigabytes", "volumes", "per_volume_gigabytes"])
    def case_int(self, key: str) -> Tuple[str, int]:
        return key, randint(0, 100)


class CaseComputeAttr:
    @parametrize(key=["cores", "instances", "ram"])
    def case_int(self, key: str) -> Tuple[str, int]:
        return key, randint(0, 100)


class CaseNetworkAttr:
    @parametrize(
        key=[
            "public_ips",
            "networks",
            "ports",
            "security_groups",
            "security_group_rules",
        ]
    )
    def case_int(self, key: str) -> Tuple[str, int]:
        return key, randint(0, 100)


def quota_dict():
    return {"type": random_lower_string()}


def test_block_storage_default_attr() -> None:
    d = quota_dict()
    item = BlockStorageQuota(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == d.get("type")
    assert item.per_user is False
    assert item.gigabytes is None
    assert item.per_volume_gigabytes is None
    assert item.volumes is None
    assert isinstance(item.service, RelationshipManager)


def test_compute_default_attr() -> None:
    d = quota_dict()
    item = ComputeQuota(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == d.get("type")
    assert item.per_user is False
    assert item.cores is None
    assert item.instances is None
    assert item.ram is None
    assert isinstance(item.service, RelationshipManager)


def test_network_default_attr() -> None:
    d = quota_dict()
    item = NetworkQuota(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == d.get("type")
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


@patch("neomodel.core.db")
@parametrize_with_cases("key, value", cases=CaseBlockStorageAttr)
def test_block_storage_attr(mock_db: Mock, key: str, value: Any) -> None:
    d = quota_dict()
    d[key] = value

    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    element_id = f"{db_version}:{uuid4().hex}:0"
    mock_db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = BlockStorageQuota(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


@patch("neomodel.core.db")
@parametrize_with_cases("key, value", cases=CaseComputeAttr)
def test_compute_attr(mock_db: Mock, key: str, value: Any) -> None:
    d = quota_dict()
    d[key] = value

    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    element_id = f"{db_version}:{uuid4().hex}:0"
    mock_db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = ComputeQuota(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


@patch("neomodel.core.db")
@parametrize_with_cases("key, value", cases=CaseNetworkAttr)
def test_network_attr(mock_db: Mock, key: str, value: Any) -> None:
    d = quota_dict()
    d[key] = value

    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    element_id = f"{db_version}:{uuid4().hex}:0"
    mock_db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = NetworkQuota(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


@patch("neomodel.match.db")
def test_block_storage_required_rel(mock_db: Mock) -> None:
    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    mock_db.cypher_query.return_value = ([], None)

    item = BlockStorageQuota(**quota_dict())
    with pytest.raises(CardinalityViolation):
        item.service.all()
    with pytest.raises(CardinalityViolation):
        item.service.single()


@patch("neomodel.match.db")
def test_compute_required_rel(mock_db: Mock) -> None:
    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    mock_db.cypher_query.return_value = ([], None)

    item = ComputeQuota(**quota_dict())
    with pytest.raises(CardinalityViolation):
        item.service.all()
    with pytest.raises(CardinalityViolation):
        item.service.single()


@patch("neomodel.match.db")
def test_network_required_rel(mock_db: Mock) -> None:
    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    mock_db.cypher_query.return_value = ([], None)

    item = NetworkQuota(**quota_dict())
    with pytest.raises(CardinalityViolation):
        item.service.all()
    with pytest.raises(CardinalityViolation):
        item.service.single()
