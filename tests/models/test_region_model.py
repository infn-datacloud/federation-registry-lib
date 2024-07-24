from unittest.mock import patch

import pytest
from neomodel import (
    AttemptedCardinalityViolation,
    CardinalityViolation,
    RelationshipManager,
)
from pytest_cases import parametrize_with_cases

from fed_reg.location.models import Location
from fed_reg.provider.models import Provider
from fed_reg.region.models import Region
from fed_reg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    ObjectStoreService,
    Service,
)
from tests.create_dict import (
    location_model_dict,
    provider_model_dict,
    region_model_dict,
)


def test_default_attr() -> None:
    d = region_model_dict()
    item = Region(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert isinstance(item.location, RelationshipManager)
    assert isinstance(item.provider, RelationshipManager)
    assert isinstance(item.services, RelationshipManager)


def test_required_rel(region_model: Region) -> None:
    with pytest.raises(CardinalityViolation):
        region_model.provider.all()
    with pytest.raises(CardinalityViolation):
        region_model.provider.single()


def test_optional_rel(region_model: Region) -> None:
    assert len(region_model.location.all()) == 0
    assert region_model.location.single() is None
    assert len(region_model.services.all()) == 0
    assert region_model.services.single() is None


@parametrize_with_cases("service_model", has_tag="single")
def test_linked_service(
    region_model: Region,
    service_model: BlockStorageService
    | ComputeService
    | IdentityService
    | NetworkService
    | ObjectStoreService,
) -> None:
    assert region_model.services.name
    assert region_model.services.source
    assert isinstance(region_model.services.source, Region)
    assert region_model.services.source.uid == region_model.uid
    assert region_model.services.definition
    assert region_model.services.definition["node_class"] == Service

    r = region_model.services.connect(service_model)
    assert r is True

    assert len(region_model.services.all()) == 1
    service = region_model.services.single()
    assert isinstance(service, Service)
    assert service.uid == service_model.uid


@parametrize_with_cases("service_models", has_tag="multi")
def test_multiple_linked_services(
    region_model: Region,
    service_models: list[BlockStorageService]
    | list[ComputeService]
    | list[IdentityService]
    | list[NetworkService]
    | list[ObjectStoreService],
) -> None:
    region_model.services.connect(service_models[0])
    region_model.services.connect(service_models[1])
    assert len(region_model.services.all()) == 2


def test_linked_location(region_model: Region, location_model: Location) -> None:
    assert region_model.location.name
    assert region_model.location.source
    assert isinstance(region_model.location.source, Region)
    assert region_model.location.source.uid == region_model.uid
    assert region_model.location.definition
    assert region_model.location.definition["node_class"] == Location

    r = region_model.location.connect(location_model)
    assert r is True

    assert len(region_model.location.all()) == 1
    location = region_model.location.single()
    assert isinstance(location, Location)
    assert location.uid == location_model.uid


def test_multiple_linked_location(region_model: Region) -> None:
    item = Location(**location_model_dict()).save()
    region_model.location.connect(item)
    item = Location(**location_model_dict()).save()
    with pytest.raises(AttemptedCardinalityViolation):
        region_model.location.connect(item)

    with patch("neomodel.sync_.match.QueryBuilder._count", return_value=0):
        region_model.location.connect(item)
        with pytest.raises(CardinalityViolation):
            region_model.location.all()


def test_linked_provider(region_model: Region, provider_model: Provider) -> None:
    assert region_model.provider.name
    assert region_model.provider.source
    assert isinstance(region_model.provider.source, Region)
    assert region_model.provider.source.uid == region_model.uid
    assert region_model.provider.definition
    assert region_model.provider.definition["node_class"] == Provider

    r = region_model.provider.connect(provider_model)
    assert r is True

    assert len(region_model.provider.all()) == 1
    provider = region_model.provider.single()
    assert isinstance(provider, Provider)
    assert provider.uid == provider_model.uid


def test_multiple_linked_provider(region_model: Region) -> None:
    item = Provider(**provider_model_dict()).save()
    region_model.provider.connect(item)
    item = Provider(**provider_model_dict()).save()
    with pytest.raises(AttemptedCardinalityViolation):
        region_model.provider.connect(item)

    with patch("neomodel.sync_.match.QueryBuilder._count", return_value=0):
        region_model.provider.connect(item)
        with pytest.raises(CardinalityViolation):
            region_model.provider.all()
