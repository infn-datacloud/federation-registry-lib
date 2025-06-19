import pytest
from neomodel import CardinalityViolation
from pytest_cases import parametrize_with_cases

from fedreg.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.flavor.models import Flavor, PrivateFlavor, SharedFlavor
from fedreg.flavor.schemas import FlavorRead, FlavorReadPublic
from fedreg.flavor.schemas_extended import (
    ComputeServiceReadExtended,
    ComputeServiceReadExtendedPublic,
    FlavorReadExtended,
    FlavorReadExtendedPublic,
    RegionReadExtended,
    RegionReadExtendedPublic,
)
from fedreg.project.models import Project
from fedreg.provider.models import Provider
from fedreg.provider.schemas import ProviderRead, ProviderReadPublic
from fedreg.region.models import Region
from fedreg.region.schemas import RegionRead, RegionReadPublic
from fedreg.service.models import ComputeService
from fedreg.service.schemas import ComputeServiceRead, ComputeServiceReadPublic


def test_class_inheritance():
    assert issubclass(FlavorReadExtended, BaseReadPrivateExtended)
    assert issubclass(FlavorReadExtended, FlavorRead)
    assert FlavorReadExtended.__fields__["schema_type"].default == "private_extended"
    assert FlavorReadExtended.__config__.orm_mode is True

    assert issubclass(FlavorReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(FlavorReadExtendedPublic, FlavorReadPublic)
    assert (
        FlavorReadExtendedPublic.__fields__["schema_type"].default == "public_extended"
    )
    assert FlavorReadExtendedPublic.__config__.orm_mode is True

    assert issubclass(ComputeServiceReadExtended, ComputeServiceRead)
    assert issubclass(ComputeServiceReadExtendedPublic, ComputeServiceReadPublic)

    assert issubclass(RegionReadExtended, RegionRead)
    assert issubclass(RegionReadExtendedPublic, RegionReadPublic)


def test_read_shared_ext(
    shared_flavor_model: SharedFlavor,
    region_model: Region,
    provider_model: Provider,
    compute_service_model: ComputeService,
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    compute_service_model.flavors.connect(shared_flavor_model)

    item = FlavorReadExtendedPublic.from_orm(shared_flavor_model)
    assert len(item.projects) == 0
    assert item.service == ComputeServiceReadExtendedPublic.from_orm(
        compute_service_model
    )

    item = FlavorReadExtended.from_orm(shared_flavor_model)
    assert item.is_shared is True
    assert len(item.projects) == 0
    assert item.service == ComputeServiceReadExtended.from_orm(compute_service_model)


@parametrize_with_cases("projects", has_tag="projects")
def test_read_private_ext(
    private_flavor_model: PrivateFlavor,
    region_model: Region,
    provider_model: Provider,
    projects: list[Project],
    compute_service_model: ComputeService,
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    compute_service_model.flavors.connect(private_flavor_model)
    for project in projects:
        private_flavor_model.projects.connect(project)

    item = FlavorReadExtendedPublic.from_orm(private_flavor_model)
    assert len(item.projects) == len(projects)
    assert item.service == ComputeServiceReadExtendedPublic.from_orm(
        compute_service_model
    )

    item = FlavorReadExtended.from_orm(private_flavor_model)
    assert item.is_shared is False
    assert len(item.projects) == len(projects)
    assert item.service == ComputeServiceReadExtended.from_orm(compute_service_model)


def test_read_ext(
    flavor_model: Flavor,
    region_model: Region,
    provider_model: Provider,
    compute_service_model: ComputeService,
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    compute_service_model.flavors.connect(flavor_model)

    item = FlavorReadExtendedPublic.from_orm(flavor_model)
    assert len(item.projects) == 0
    assert item.service == ComputeServiceReadExtendedPublic.from_orm(
        compute_service_model
    )

    item = FlavorReadExtended.from_orm(flavor_model)
    assert item.is_shared is None
    assert len(item.projects) == 0
    assert item.service == ComputeServiceReadExtended.from_orm(compute_service_model)


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


def test_compute_serv_read_ext(
    provider_model: Provider,
    region_model: Region,
    compute_service_model: ComputeService,
):
    with pytest.raises(CardinalityViolation):
        ComputeServiceReadExtended.from_orm(compute_service_model)
    region_model.services.connect(compute_service_model)
    with pytest.raises(CardinalityViolation):
        ComputeServiceReadExtended.from_orm(compute_service_model)
    provider_model.regions.connect(region_model)
    service = ComputeServiceReadExtended.from_orm(compute_service_model)
    assert service.region == RegionReadExtended.from_orm(region_model)


def test_compute_serv_read_ext_public(
    provider_model: Provider,
    region_model: Region,
    compute_service_model: ComputeService,
):
    with pytest.raises(CardinalityViolation):
        ComputeServiceReadExtendedPublic.from_orm(compute_service_model)
    region_model.services.connect(compute_service_model)
    with pytest.raises(CardinalityViolation):
        ComputeServiceReadExtendedPublic.from_orm(compute_service_model)
    provider_model.regions.connect(region_model)
    service = ComputeServiceReadExtendedPublic.from_orm(compute_service_model)
    assert service.region == RegionReadExtendedPublic.from_orm(region_model)
