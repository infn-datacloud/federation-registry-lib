from typing import Any, Tuple
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
)
from tests.create_dict import service_dict
from tests.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["type", "endpoint", "name"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(key=["description"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()


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


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_block_storage_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = service_dict()
    d[key] = value

    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = BlockStorageService(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_compute_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = service_dict()
    d[key] = value

    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = ComputeService(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_identity_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = service_dict()
    d[key] = value

    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = IdentityService(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_network_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = service_dict()
    d[key] = value

    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = NetworkService(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_block_storage_required_rel(
    db_match: MagicMock, block_storage_service_model: BlockStorageService
) -> None:
    db_match.cypher_query.return_value = ([], None)
    with pytest.raises(CardinalityViolation):
        block_storage_service_model.region.all()
    with pytest.raises(CardinalityViolation):
        block_storage_service_model.region.single()


def test_block_storage_optional_rel(
    db_match: MagicMock, block_storage_service_model: BlockStorageService
) -> None:
    db_match.cypher_query.return_value = ([], None)
    assert len(block_storage_service_model.quotas.all()) == 0
    assert block_storage_service_model.quotas.single() is None


def test_compute_required_rel(
    db_match: MagicMock, compute_service_model: ComputeService
) -> None:
    db_match.cypher_query.return_value = ([], None)
    with pytest.raises(CardinalityViolation):
        compute_service_model.region.all()
    with pytest.raises(CardinalityViolation):
        compute_service_model.region.single()


def test_compute_optional_rel(
    db_match: MagicMock, compute_service_model: ComputeService
) -> None:
    db_match.cypher_query.return_value = ([], None)
    assert len(compute_service_model.quotas.all()) == 0
    assert compute_service_model.quotas.single() is None
    assert len(compute_service_model.flavors.all()) == 0
    assert compute_service_model.flavors.single() is None
    assert len(compute_service_model.images.all()) == 0
    assert compute_service_model.images.single() is None


def test_identity_required_rel(
    db_match: MagicMock, identity_service_model: IdentityService
) -> None:
    db_match.cypher_query.return_value = ([], None)
    with pytest.raises(CardinalityViolation):
        identity_service_model.region.all()
    with pytest.raises(CardinalityViolation):
        identity_service_model.region.single()


def test_network_required_rel(
    db_match: MagicMock, network_service_model: NetworkService
) -> None:
    db_match.cypher_query.return_value = ([], None)
    with pytest.raises(CardinalityViolation):
        network_service_model.region.all()
    with pytest.raises(CardinalityViolation):
        network_service_model.region.single()


def test_network_optional_rel(
    db_match: MagicMock, network_service_model: NetworkService
) -> None:
    db_match.cypher_query.return_value = ([], None)
    assert len(network_service_model.quotas.all()) == 0
    assert network_service_model.quotas.single() is None
    assert len(network_service_model.networks.all()) == 0
    assert network_service_model.networks.single() is None
