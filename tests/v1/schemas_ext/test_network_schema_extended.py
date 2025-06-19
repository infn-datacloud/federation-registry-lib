import pytest
from neomodel import CardinalityViolation
from pytest_cases import parametrize_with_cases

from fedreg.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.network.models import Network, PrivateNetwork, SharedNetwork
from fedreg.network.schemas import NetworkRead, NetworkReadPublic
from fedreg.network.schemas_extended import (
    NetworkReadExtended,
    NetworkReadExtendedPublic,
    NetworkServiceReadExtended,
    NetworkServiceReadExtendedPublic,
    RegionReadExtended,
    RegionReadExtendedPublic,
)
from fedreg.project.models import Project
from fedreg.provider.models import Provider
from fedreg.provider.schemas import ProviderRead, ProviderReadPublic
from fedreg.region.models import Region
from fedreg.region.schemas import RegionRead, RegionReadPublic
from fedreg.service.models import NetworkService
from fedreg.service.schemas import NetworkServiceRead, NetworkServiceReadPublic


def test_class_inheritance():
    assert issubclass(NetworkReadExtended, BaseReadPrivateExtended)
    assert issubclass(NetworkReadExtended, NetworkRead)
    assert NetworkReadExtended.__fields__["schema_type"].default == "private_extended"

    assert issubclass(NetworkReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(NetworkReadExtendedPublic, NetworkReadPublic)
    assert (
        NetworkReadExtendedPublic.__fields__["schema_type"].default == "public_extended"
    )

    assert issubclass(NetworkServiceReadExtended, NetworkServiceRead)
    assert issubclass(NetworkServiceReadExtendedPublic, NetworkServiceReadPublic)

    assert issubclass(RegionReadExtended, RegionRead)
    assert issubclass(RegionReadExtendedPublic, RegionReadPublic)


def test_read_shared_ext(
    shared_network_model: SharedNetwork,
    region_model: Region,
    provider_model: Provider,
    network_service_model: NetworkService,
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    network_service_model.networks.connect(shared_network_model)

    item = NetworkReadExtendedPublic.from_orm(shared_network_model)
    assert len(item.projects) == 0
    assert item.service == NetworkServiceReadExtendedPublic.from_orm(
        network_service_model
    )

    item = NetworkReadExtended.from_orm(shared_network_model)
    assert item.is_shared is True
    assert len(item.projects) == 0
    assert item.service == NetworkServiceReadExtended.from_orm(network_service_model)


@parametrize_with_cases("projects", has_tag="projects")
def test_read_private_ext(
    private_network_model: PrivateNetwork,
    region_model: Region,
    provider_model: Provider,
    network_service_model: NetworkService,
    projects: list[Project],
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    network_service_model.networks.connect(private_network_model)
    for project in projects:
        private_network_model.projects.connect(project)

    item = NetworkReadExtendedPublic.from_orm(private_network_model)
    assert len(item.projects) == len(projects)
    assert item.service == NetworkServiceReadExtendedPublic.from_orm(
        network_service_model
    )

    item = NetworkReadExtended.from_orm(private_network_model)
    assert item.is_shared is False
    assert len(item.projects) == len(projects)
    assert item.service == NetworkServiceReadExtended.from_orm(network_service_model)


def test_read_ext(
    network_model: Network,
    region_model: Region,
    provider_model: Provider,
    network_service_model: NetworkService,
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    network_service_model.networks.connect(network_model)

    item = NetworkReadExtendedPublic.from_orm(network_model)
    assert len(item.projects) == 0
    assert item.service == NetworkServiceReadExtendedPublic.from_orm(
        network_service_model
    )

    item = NetworkReadExtended.from_orm(network_model)
    assert item.is_shared is None
    assert len(item.projects) == 0
    assert item.service == NetworkServiceReadExtended.from_orm(network_service_model)


def test_region_read_ext(provider_model: Provider, region_model: Region):
    with pytest.raises(CardinalityViolation):
        RegionReadExtended.from_orm(region_model)
    provider_model.regions.connect(region_model)
    region = RegionReadExtended.from_orm(region_model)
    assert region.provider == ProviderRead.from_orm(provider_model)


def test_region_read_ext_public(provider_model: Provider, region_model: Region):
    with pytest.raises(CardinalityViolation):
        RegionReadExtendedPublic.from_orm(region_model)
    provider_model.regions.connect(region_model)
    region = RegionReadExtendedPublic.from_orm(region_model)
    assert region.provider == ProviderReadPublic.from_orm(provider_model)


def test_network_serv_read_ext(
    provider_model: Provider,
    region_model: Region,
    network_service_model: NetworkService,
):
    with pytest.raises(CardinalityViolation):
        NetworkServiceReadExtended.from_orm(network_service_model)
    region_model.services.connect(network_service_model)
    with pytest.raises(CardinalityViolation):
        NetworkServiceReadExtended.from_orm(network_service_model)
    provider_model.regions.connect(region_model)
    service = NetworkServiceReadExtended.from_orm(network_service_model)
    assert service.region == RegionReadExtended.from_orm(region_model)


def test_network_serv_read_ext_public(
    provider_model: Provider,
    region_model: Region,
    network_service_model: NetworkService,
):
    with pytest.raises(CardinalityViolation):
        NetworkServiceReadExtendedPublic.from_orm(network_service_model)
    region_model.services.connect(network_service_model)
    with pytest.raises(CardinalityViolation):
        NetworkServiceReadExtendedPublic.from_orm(network_service_model)
    provider_model.regions.connect(region_model)
    service = NetworkServiceReadExtendedPublic.from_orm(network_service_model)
    assert service.region == RegionReadExtendedPublic.from_orm(region_model)
