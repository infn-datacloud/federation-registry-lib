import pytest
from neomodel import CardinalityViolation
from pytest_cases import parametrize_with_cases

from fedreg.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.image.models import Image, PrivateImage, SharedImage
from fedreg.image.schemas import ImageRead, ImageReadPublic
from fedreg.image.schemas_extended import (
    ComputeServiceReadExtended,
    ComputeServiceReadExtendedPublic,
    ImageReadExtended,
    ImageReadExtendedPublic,
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
    assert issubclass(ImageReadExtended, BaseReadPrivateExtended)
    assert issubclass(ImageReadExtended, ImageRead)
    assert ImageReadExtended.__fields__["schema_type"].default == "private_extended"

    assert issubclass(ImageReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(ImageReadExtendedPublic, ImageReadPublic)
    assert (
        ImageReadExtendedPublic.__fields__["schema_type"].default == "public_extended"
    )

    assert issubclass(ComputeServiceReadExtended, ComputeServiceRead)
    assert issubclass(ComputeServiceReadExtendedPublic, ComputeServiceReadPublic)

    assert issubclass(RegionReadExtended, RegionRead)
    assert issubclass(RegionReadExtendedPublic, RegionReadPublic)


@parametrize_with_cases("services", has_tag="services")
def test_read_shared_ext(
    shared_image_model: SharedImage,
    region_model: Region,
    provider_model: Provider,
    services: list[ComputeService],
) -> None:
    for service in services:
        provider_model.regions.connect(region_model)
        region_model.services.connect(service)
        service.images.connect(shared_image_model)

    item = ImageReadExtendedPublic.from_orm(shared_image_model)
    assert len(item.projects) == 0
    assert len(item.services) == len(services)

    item = ImageReadExtended.from_orm(shared_image_model)
    assert item.is_shared is True
    assert len(item.projects) == 0
    assert len(item.services) == len(services)


@parametrize_with_cases("services", has_tag="services")
@parametrize_with_cases("projects", has_tag="projects")
def test_read_private_ext(
    private_image_model: PrivateImage,
    region_model: Region,
    provider_model: Provider,
    projects: list[Project],
    services: list[ComputeService],
) -> None:
    for service in services:
        provider_model.regions.connect(region_model)
        region_model.services.connect(service)
        service.images.connect(private_image_model)
    for project in projects:
        private_image_model.projects.connect(project)

    item = ImageReadExtendedPublic.from_orm(private_image_model)
    assert len(item.projects) == len(projects)
    assert len(item.services) == len(services)

    item = ImageReadExtended.from_orm(private_image_model)
    assert item.is_shared is False
    assert len(item.projects) == len(projects)
    assert len(item.services) == len(services)


@parametrize_with_cases("services", has_tag="services")
def test_read_ext(
    image_model: Image,
    region_model: Region,
    provider_model: Provider,
    services: list[ComputeService],
) -> None:
    for service in services:
        provider_model.regions.connect(region_model)
        region_model.services.connect(service)
        service.images.connect(image_model)

    item = ImageReadExtendedPublic.from_orm(image_model)
    assert len(item.projects) == 0
    assert len(item.services) == len(services)

    item = ImageReadExtended.from_orm(image_model)
    assert item.is_shared is None
    assert len(item.projects) == 0
    assert len(item.services) == len(services)


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
