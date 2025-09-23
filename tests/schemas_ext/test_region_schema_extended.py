from pytest_cases import parametrize_with_cases

from fedreg.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.location.models import Location
from fedreg.location.schemas import LocationRead, LocationReadPublic
from fedreg.provider.models import Provider
from fedreg.provider.schemas import ProviderRead, ProviderReadPublic
from fedreg.region.models import Region
from fedreg.region.schemas import RegionRead, RegionReadPublic
from fedreg.region.schemas_extended import (
    RegionReadExtended,
    RegionReadExtendedPublic,
)
from fedreg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    ObjectStoreService,
)


def test_class_inheritance():
    assert issubclass(RegionReadExtended, BaseReadPrivateExtended)
    assert issubclass(RegionReadExtended, RegionRead)
    assert RegionReadExtended.__fields__["schema_type"].default == "private_extended"
    assert RegionReadExtended.__config__.orm_mode is True

    assert issubclass(RegionReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(RegionReadExtendedPublic, RegionReadPublic)
    assert (
        RegionReadExtendedPublic.__fields__["schema_type"].default == "public_extended"
    )
    assert RegionReadExtendedPublic.__config__.orm_mode is True


@parametrize_with_cases("location", has_tag="location")
def test_read_ext(
    region_model: Region, provider_model: Provider, location: Location | None
) -> None:
    region_model.provider.connect(provider_model)
    if location is not None:
        region_model.location.connect(location)

    item = RegionReadExtendedPublic.from_orm(region_model)
    assert item.provider == ProviderReadPublic.from_orm(provider_model)
    if location is None:
        assert item.location is None
    else:
        assert item.location == LocationReadPublic.from_orm(location)
    assert len(item.services) == 0

    item = RegionReadExtended.from_orm(region_model)
    assert item.provider == ProviderRead.from_orm(provider_model)
    if location is None:
        assert item.location is None
    else:
        assert item.location == LocationRead.from_orm(location)
    assert len(item.services) == 0


@parametrize_with_cases("services", has_tag="services")
def test_read_ext_with_services(
    region_model: Region,
    provider_model: Provider,
    services: list[BlockStorageService]
    | list[ComputeService]
    | list[IdentityService]
    | list[NetworkService]
    | list[ObjectStoreService]
    | list[
        BlockStorageService
        | ComputeService
        | IdentityService
        | NetworkService
        | ObjectStoreService
    ],
) -> None:
    region_model.provider.connect(provider_model)
    for service in services:
        region_model.services.connect(service)

    item = RegionReadExtendedPublic.from_orm(region_model)
    assert item.provider == ProviderReadPublic.from_orm(provider_model)
    assert item.location is None
    assert len(item.services) == len(services)
    item = RegionReadExtended.from_orm(region_model)
    assert item.provider == ProviderRead.from_orm(provider_model)
    assert item.location is None
    assert len(item.services) == len(services)
