from typing import Any, Union
from unittest.mock import patch

import pytest
from neomodel import (
    AttemptedCardinalityViolation,
    CardinalityViolation,
    RelationshipManager,
    RequiredProperty,
)
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.location.models import Location
from fed_reg.provider.models import Provider
from fed_reg.region.models import Region
from fed_reg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    Service,
)
from tests.create_dict import (
    block_storage_service_model_dict,
    compute_service_model_dict,
    identity_service_model_dict,
    location_model_dict,
    network_service_model_dict,
    provider_model_dict,
    region_model_dict,
)
from tests.utils import random_lower_string


class CaseAttr:
    @parametrize(key=["description"])
    def case_str(self, key: str) -> tuple[str, str]:
        return key, random_lower_string()


class CaseServiceModel:
    @case(tags=["single"])
    def case_block_storage_service(
        self, block_storage_service_model: BlockStorageService
    ) -> BlockStorageService:
        return block_storage_service_model

    @case(tags=["single"])
    def case_compute_service(
        self, compute_service_model: ComputeService
    ) -> ComputeService:
        return compute_service_model

    @case(tags=["single"])
    def case_identity_service(
        self, identity_service_model: IdentityService
    ) -> IdentityService:
        return identity_service_model

    @case(tags=["single"])
    def case_network_service(
        self, network_service_model: NetworkService
    ) -> NetworkService:
        return network_service_model

    @case(tags=["multi"])
    def case_block_storage_services(self) -> list[BlockStorageService]:
        return [
            BlockStorageService(**block_storage_service_model_dict()).save(),
            BlockStorageService(**block_storage_service_model_dict()).save(),
        ]

    @case(tags=["multi"])
    def case_compute_services(self) -> list[ComputeService]:
        return [
            ComputeService(**compute_service_model_dict()).save(),
            ComputeService(**compute_service_model_dict()).save(),
        ]

    @case(tags=["multi"])
    def case_identity_services(self) -> list[IdentityService]:
        return [
            IdentityService(**identity_service_model_dict()).save(),
            IdentityService(**identity_service_model_dict()).save(),
        ]

    @case(tags=["multi"])
    def case_network_services(self) -> list[NetworkService]:
        return [
            NetworkService(**network_service_model_dict()).save(),
            NetworkService(**network_service_model_dict()).save(),
        ]


def test_default_attr() -> None:
    d = region_model_dict()
    item = Region(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert isinstance(item.location, RelationshipManager)
    assert isinstance(item.provider, RelationshipManager)
    assert isinstance(item.services, RelationshipManager)


def test_missing_attr() -> None:
    item = Region()
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(key: str, value: Any) -> None:
    d = region_model_dict()
    d[key] = value

    item = Region(**d)
    saved = item.save()

    assert saved.element_id_property
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


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


@parametrize_with_cases("service_model", cases=CaseServiceModel, has_tag="single")
def test_linked_service(
    region_model: Region,
    service_model: Union[
        BlockStorageService, ComputeService, IdentityService, NetworkService
    ],
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


@parametrize_with_cases("service_models", cases=CaseServiceModel, has_tag="multi")
def test_multiple_linked_services(
    region_model: Region,
    service_models: Union[
        BlockStorageService, ComputeService, IdentityService, NetworkService
    ],
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

    with patch("neomodel.match.QueryBuilder._count", return_value=0):
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

    with patch("neomodel.match.QueryBuilder._count", return_value=0):
        region_model.provider.connect(item)
        with pytest.raises(CardinalityViolation):
            region_model.provider.all()
