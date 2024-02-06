import pytest
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


def test_block_storage_default_attr() -> None:
    d = {
        "type": random_lower_string(),
        "endpoint": random_lower_string(),
        "name": random_lower_string(),
    }
    item = BlockStorageService(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == d.get("type")
    assert item.endpoint == d.get("endpoint")
    assert item.name == d.get("name")
    assert isinstance(item.region, RelationshipManager)
    assert isinstance(item.quotas, RelationshipManager)


def test_compute_default_attr() -> None:
    d = {
        "type": random_lower_string(),
        "endpoint": random_lower_string(),
        "name": random_lower_string(),
    }
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
    d = {
        "type": random_lower_string(),
        "endpoint": random_lower_string(),
        "name": random_lower_string(),
    }
    item = IdentityService(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.type == d.get("type")
    assert item.endpoint == d.get("endpoint")
    assert item.name == d.get("name")
    assert isinstance(item.region, RelationshipManager)


def test_network_default_attr() -> None:
    d = {
        "type": random_lower_string(),
        "endpoint": random_lower_string(),
        "name": random_lower_string(),
    }
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
    d = {
        "type": None if missing_attr == "type" else random_lower_string(),
        "endpoint": None if missing_attr == "endpoint" else random_lower_string(),
        "name": None if missing_attr == "name" else random_lower_string(),
    }
    item = BlockStorageService(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_compute_missing_attr(missing_attr: str) -> None:
    d = {
        "type": None if missing_attr == "type" else random_lower_string(),
        "endpoint": None if missing_attr == "endpoint" else random_lower_string(),
        "name": None if missing_attr == "name" else random_lower_string(),
    }
    item = ComputeService(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_identity_missing_attr(missing_attr: str) -> None:
    d = {
        "type": None if missing_attr == "type" else random_lower_string(),
        "endpoint": None if missing_attr == "endpoint" else random_lower_string(),
        "name": None if missing_attr == "name" else random_lower_string(),
    }
    item = IdentityService(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_network_missing_attr(missing_attr: str) -> None:
    d = {
        "type": None if missing_attr == "type" else random_lower_string(),
        "endpoint": None if missing_attr == "endpoint" else random_lower_string(),
        "name": None if missing_attr == "name" else random_lower_string(),
    }
    item = NetworkService(**d)
    with pytest.raises(RequiredProperty):
        item.save()
