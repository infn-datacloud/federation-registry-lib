from typing import Any, Tuple, Union
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import (
    AttemptedCardinalityViolation,
    CardinalityViolation,
    RelationshipManager,
    RequiredProperty,
)
from pytest_cases import parametrize, parametrize_with_cases

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
from tests.create_dict import region_model_dict
from tests.utils import random_lower_string


class CaseAttr:
    @parametrize(key=["description"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()


class CaseServiceModel:
    def case_block_storage_service(
        self, block_storage_service_model: BlockStorageService
    ) -> BlockStorageService:
        return block_storage_service_model

    def case_compute_service(
        self, compute_service_model: ComputeService
    ) -> ComputeService:
        return compute_service_model

    def case_identity_service(
        self, identity_service_model: IdentityService
    ) -> IdentityService:
        return identity_service_model

    def case_network_service(
        self, network_service_model: NetworkService
    ) -> NetworkService:
        return network_service_model


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
def test_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = region_model_dict()
    d[key] = value

    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = Region(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel(db_match: MagicMock, region_model: Region) -> None:
    db_match.cypher_query.return_value = ([], None)
    with pytest.raises(CardinalityViolation):
        region_model.provider.all()
    with pytest.raises(CardinalityViolation):
        region_model.provider.single()


def test_optional_rel(db_match: MagicMock, region_model: Region) -> None:
    db_match.cypher_query.return_value = ([], None)
    assert len(region_model.location.all()) == 0
    assert region_model.location.single() is None
    assert len(region_model.services.all()) == 0
    assert region_model.services.single() is None


@parametrize_with_cases("service_model", cases=CaseServiceModel)
def test_linked_service(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
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

    db_match.cypher_query.return_value = ([[service_model]], ["services_r1"])
    assert len(region_model.services.all()) == 1
    service = region_model.services.single()
    assert isinstance(service, Service)
    assert service.uid == service_model.uid


@parametrize_with_cases("service_model", cases=CaseServiceModel)
def test_multiple_linked_services(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    region_model: Region,
    service_model: Union[
        BlockStorageService, ComputeService, IdentityService, NetworkService
    ],
) -> None:
    db_match.cypher_query.return_value = (
        [[service_model], [service_model]],
        ["services_r1", "services_r2"],
    )
    assert len(region_model.services.all()) == 2


@patch("neomodel.match.QueryBuilder._count", return_value=0)
def test_linked_location(
    mock_count: MagicMock,
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    region_model: Region,
    location_model: Location,
) -> None:
    assert region_model.location.name
    assert region_model.location.source
    assert isinstance(region_model.location.source, Region)
    assert region_model.location.source.uid == region_model.uid
    assert region_model.location.definition
    assert region_model.location.definition["node_class"] == Location

    r = region_model.location.connect(location_model)
    assert r is True

    db_match.cypher_query.return_value = ([[location_model]], ["location_r1"])
    assert len(region_model.location.all()) == 1
    location = region_model.location.single()
    assert isinstance(location, Location)
    assert location.uid == location_model.uid


def test_multiple_linked_location(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    region_model: Region,
    location_model: Location,
) -> None:
    with patch("neomodel.match.QueryBuilder._count") as mock_count:
        mock_count.return_value = 1
        with pytest.raises(AttemptedCardinalityViolation):
            region_model.location.connect(location_model)

    db_match.cypher_query.return_value = (
        [[location_model], [location_model]],
        ["location_r1", "location_r2"],
    )
    with pytest.raises(CardinalityViolation):
        region_model.location.all()


@patch("neomodel.match.QueryBuilder._count", return_value=0)
def test_linked_provider(
    mock_count: MagicMock,
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    region_model: Region,
    provider_model: Provider,
) -> None:
    assert region_model.provider.name
    assert region_model.provider.source
    assert isinstance(region_model.provider.source, Region)
    assert region_model.provider.source.uid == region_model.uid
    assert region_model.provider.definition
    assert region_model.provider.definition["node_class"] == Provider

    r = region_model.provider.connect(provider_model)
    assert r is True

    db_match.cypher_query.return_value = ([[provider_model]], ["provider_r1"])
    assert len(region_model.provider.all()) == 1
    provider = region_model.provider.single()
    assert isinstance(provider, Provider)
    assert provider.uid == provider_model.uid


def test_multiple_linked_provider(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    region_model: Region,
    provider_model: Provider,
) -> None:
    with patch("neomodel.match.QueryBuilder._count") as mock_count:
        mock_count.return_value = 1
        with pytest.raises(AttemptedCardinalityViolation):
            region_model.provider.connect(provider_model)

    db_match.cypher_query.return_value = (
        [[provider_model], [provider_model]],
        ["provider_r1", "provider_r2"],
    )
    with pytest.raises(CardinalityViolation):
        region_model.provider.all()
