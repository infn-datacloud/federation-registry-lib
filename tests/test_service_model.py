from typing import Any, Dict, Tuple
from unittest.mock import Mock, PropertyMock, patch
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from app.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
)
from tests.common.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["type", "endpoint", "name"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(key=["description"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()


def service_dict() -> Dict[str, str]:
    return {
        "type": random_lower_string(),
        "endpoint": random_lower_string(),
        "name": random_lower_string(),
    }


def test_block_storage_default_attr() -> None:
    d = service_dict()
    item = BlockStorageService(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == d.get("type")
    assert item.endpoint == d.get("endpoint")
    assert item.name == d.get("name")
    assert isinstance(item.region, RelationshipManager)
    assert isinstance(item.quotas, RelationshipManager)


def test_compute_default_attr() -> None:
    d = service_dict()
    item = ComputeService(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == d.get("type")
    assert item.endpoint == d.get("endpoint")
    assert item.name == d.get("name")
    assert isinstance(item.region, RelationshipManager)
    assert isinstance(item.flavors, RelationshipManager)
    assert isinstance(item.images, RelationshipManager)
    assert isinstance(item.quotas, RelationshipManager)


def test_identity_default_attr() -> None:
    d = service_dict()
    item = IdentityService(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == d.get("type")
    assert item.endpoint == d.get("endpoint")
    assert item.name == d.get("name")
    assert isinstance(item.region, RelationshipManager)


def test_network_default_attr() -> None:
    d = service_dict()
    item = NetworkService(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == d.get("type")
    assert item.endpoint == d.get("endpoint")
    assert item.name == d.get("name")
    assert isinstance(item.region, RelationshipManager)
    assert isinstance(item.networks, RelationshipManager)
    assert isinstance(item.quotas, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_block_storage_missing_attr(missing_attr: str) -> None:
    d = service_dict()
    d[missing_attr] = None
    item = BlockStorageService(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_compute_missing_attr(missing_attr: str) -> None:
    d = service_dict()
    d[missing_attr] = None
    item = ComputeService(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_identity_missing_attr(missing_attr: str) -> None:
    d = service_dict()
    d[missing_attr] = None
    item = IdentityService(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_network_missing_attr(missing_attr: str) -> None:
    d = service_dict()
    d[missing_attr] = None
    item = NetworkService(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@patch("neomodel.core.db")
@parametrize_with_cases("key, value", cases=CaseAttr)
def test_block_storage_attr(mock_db: Mock, key: str, value: Any) -> None:
    d = service_dict()
    d[key] = value

    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    element_id = f"{db_version}:{uuid4().hex}:0"
    mock_db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = BlockStorageService(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


@patch("neomodel.core.db")
@parametrize_with_cases("key, value", cases=CaseAttr)
def test_compute_attr(mock_db: Mock, key: str, value: Any) -> None:
    d = service_dict()
    d[key] = value

    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    element_id = f"{db_version}:{uuid4().hex}:0"
    mock_db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = ComputeService(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


@patch("neomodel.core.db")
@parametrize_with_cases("key, value", cases=CaseAttr)
def test_identity_attr(mock_db: Mock, key: str, value: Any) -> None:
    d = service_dict()
    d[key] = value

    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    element_id = f"{db_version}:{uuid4().hex}:0"
    mock_db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = IdentityService(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


@patch("neomodel.core.db")
@parametrize_with_cases("key, value", cases=CaseAttr)
def test_network_attr(mock_db: Mock, key: str, value: Any) -> None:
    d = service_dict()
    d[key] = value

    db_version = "5"
    type(mock_db).database_version = PropertyMock(return_value=db_version)
    element_id = f"{db_version}:{uuid4().hex}:0"
    mock_db.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = NetworkService(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value
