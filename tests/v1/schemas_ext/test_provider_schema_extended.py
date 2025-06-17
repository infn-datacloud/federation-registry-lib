import pytest
from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from fedreg.v1.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.v1.identity_provider.models import IdentityProvider
from fedreg.v1.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from fedreg.v1.location.models import Location
from fedreg.v1.location.schemas import LocationRead, LocationReadPublic
from fedreg.v1.project.models import Project
from fedreg.v1.provider.models import Provider
from fedreg.v1.provider.schemas import ProviderRead, ProviderReadPublic
from fedreg.v1.provider.schemas_extended import (
    BlockStorageServiceReadExtended,
    BlockStorageServiceReadExtendedPublic,
    ComputeServiceReadExtended,
    ComputeServiceReadExtendedPublic,
    IdentityProviderReadExtended,
    IdentityProviderReadExtendedPublic,
    NetworkServiceReadExtended,
    NetworkServiceReadExtendedPublic,
    ObjectStoreServiceReadExtended,
    ObjectStoreServiceReadExtendedPublic,
    ProviderReadExtended,
    ProviderReadExtendedPublic,
    RegionReadExtended,
    RegionReadExtendedPublic,
    UserGroupReadExtended,
    UserGroupReadExtendedPublic,
)
from fedreg.v1.quota.models import (
    BlockStorageQuota,
    ComputeQuota,
    NetworkQuota,
    ObjectStoreQuota,
)
from fedreg.v1.quota.schemas import (
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
    ObjectStoreQuotaRead,
    ObjectStoreQuotaReadPublic,
)
from fedreg.v1.region.models import Region
from fedreg.v1.region.schemas import RegionRead, RegionReadPublic
from fedreg.v1.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    ObjectStoreService,
)
from fedreg.v1.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    NetworkServiceRead,
    NetworkServiceReadPublic,
    ObjectStoreServiceRead,
    ObjectStoreServiceReadPublic,
)
from fedreg.v1.sla.models import SLA
from fedreg.v1.sla.schemas import SLARead, SLAReadPublic
from fedreg.v1.user_group.models import UserGroup
from fedreg.v1.user_group.schemas import UserGroupRead, UserGroupReadPublic
from tests.v1.models.utils import auth_method_model_dict


def test_class_inheritance():
    assert issubclass(ProviderReadExtended, BaseReadPrivateExtended)
    assert issubclass(ProviderReadExtended, ProviderRead)
    assert ProviderReadExtended.__fields__["schema_type"].default == "private_extended"
    assert ProviderReadExtended.__config__.orm_mode is True

    assert issubclass(ProviderReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(ProviderReadExtendedPublic, ProviderReadPublic)
    assert (
        ProviderReadExtendedPublic.__fields__["schema_type"].default
        == "public_extended"
    )
    assert ProviderReadExtendedPublic.__config__.orm_mode is True

    assert issubclass(ProviderReadExtended, ProviderRead)
    assert issubclass(ProviderReadExtendedPublic, ProviderReadPublic)

    assert issubclass(RegionReadExtended, RegionRead)
    assert issubclass(RegionReadExtendedPublic, RegionReadPublic)

    assert issubclass(UserGroupReadExtended, UserGroupRead)
    assert issubclass(UserGroupReadExtendedPublic, UserGroupReadPublic)

    assert issubclass(IdentityProviderReadExtended, IdentityProviderRead)
    assert issubclass(IdentityProviderReadExtendedPublic, IdentityProviderReadPublic)

    assert issubclass(BlockStorageServiceReadExtended, BlockStorageServiceRead)
    assert issubclass(
        BlockStorageServiceReadExtendedPublic, BlockStorageServiceReadPublic
    )

    assert issubclass(ComputeServiceReadExtended, ComputeServiceRead)
    assert issubclass(ComputeServiceReadExtendedPublic, ComputeServiceReadPublic)

    assert issubclass(NetworkServiceReadExtended, NetworkServiceRead)
    assert issubclass(NetworkServiceReadExtendedPublic, NetworkServiceReadPublic)

    assert issubclass(ObjectStoreServiceReadExtended, ObjectStoreServiceRead)
    assert issubclass(
        ObjectStoreServiceReadExtendedPublic, ObjectStoreServiceReadPublic
    )


def test_read_ext(
    provider_model: Provider,
) -> None:
    item = ProviderReadExtendedPublic.from_orm(provider_model)
    assert item.regions is not None
    assert len(item.regions) == 0
    assert item.projects is not None
    assert len(item.projects) == 0
    assert item.identity_providers is not None
    assert len(item.identity_providers) == 0

    item = ProviderReadExtended.from_orm(provider_model)
    assert item.regions is not None
    assert len(item.regions) == 0
    assert item.projects is not None
    assert len(item.projects) == 0
    assert item.identity_providers is not None
    assert len(item.identity_providers) == 0


@parametrize_with_cases("regions", has_tag="regions")
def test_read_ext_with_reg(
    provider_model: Provider,
    regions: list[Region],
) -> None:
    for region in regions:
        provider_model.regions.connect(region)

    item = ProviderReadExtendedPublic.from_orm(provider_model)
    assert item.regions is not None
    assert len(item.regions) == len(regions)
    assert item.projects is not None
    assert len(item.projects) == 0
    assert item.identity_providers is not None
    assert len(item.identity_providers) == 0

    item = ProviderReadExtended.from_orm(provider_model)
    assert item.regions is not None
    assert len(item.regions) == len(regions)
    assert item.projects is not None
    assert len(item.projects) == 0
    assert item.identity_providers is not None
    assert len(item.identity_providers) == 0


@parametrize_with_cases("projects", has_tag="projects")
def test_read_ext_with_proj(
    provider_model: Provider,
    projects: list[Project],
) -> None:
    for project in projects:
        provider_model.projects.connect(project)

    item = ProviderReadExtendedPublic.from_orm(provider_model)
    assert item.regions is not None
    assert len(item.regions) == 0
    assert item.projects is not None
    assert len(item.projects) == len(projects)
    assert item.identity_providers is not None
    assert len(item.identity_providers) == 0

    item = ProviderReadExtended.from_orm(provider_model)
    assert item.regions is not None
    assert len(item.regions) == 0
    assert item.projects is not None
    assert len(item.projects) == len(projects)
    assert item.identity_providers is not None
    assert len(item.identity_providers) == 0


@parametrize_with_cases("identity_providers", has_tag="identity_providers")
def test_read_ext_with_idp(
    provider_model: Provider,
    identity_providers: list[IdentityProvider],
) -> None:
    for identity_provider in identity_providers:
        provider_model.identity_providers.connect(
            identity_provider, auth_method_model_dict()
        )

    item = ProviderReadExtendedPublic.from_orm(provider_model)
    assert item.regions is not None
    assert len(item.regions) == 0
    assert item.projects is not None
    assert len(item.projects) == 0
    assert item.identity_providers is not None
    assert len(item.identity_providers) == len(identity_providers)

    item = ProviderReadExtended.from_orm(provider_model)
    assert item.regions is not None
    assert len(item.regions) == 0
    assert item.projects is not None
    assert len(item.projects) == 0
    assert item.identity_providers is not None
    assert len(item.identity_providers) == len(identity_providers)


@parametrize_with_cases("location", has_tag="location")
def test_region_read_ext(
    region_model: Region,
    provider_model: Provider,
    location: Location | None,
):
    if location:
        region_model.location.connect(location)
    region = RegionReadExtended.from_orm(region_model)
    region_model.provider.connect(provider_model)
    provider = ProviderReadExtended.from_orm(provider_model)
    assert len(provider.regions) == 1
    assert provider.regions[0] == region
    if location:
        assert isinstance(provider.regions[0].location, LocationRead)
    assert len(provider.regions[0].services) == 0


@parametrize_with_cases("location", has_tag="location")
def test_region_read_ext_public(
    region_model: Region, provider_model: Provider, location: Location | None
):
    if location:
        region_model.location.connect(location)
    region = RegionReadExtendedPublic.from_orm(region_model)
    region_model.provider.connect(provider_model)
    provider = ProviderReadExtendedPublic.from_orm(provider_model)
    assert len(provider.regions) == 1
    assert provider.regions[0] == region
    if location:
        assert isinstance(provider.regions[0].location, LocationReadPublic)
    assert len(provider.regions[0].services) == 0


@parametrize_with_cases("services", has_tag="services")
def test_region_read_ext_with_srv(
    region_model: Region,
    provider_model: Provider,
    services: list[BlockStorageService]
    | list[ComputeService]
    | list[IdentityService]
    | list[NetworkService]
    | list[ObjectStoreService]
    | list[
        BlockStorageService,
        ComputeService,
        IdentityService,
        NetworkService,
        ObjectStoreService,
    ],
):
    for service in services:
        region_model.services.connect(service)
    region = RegionReadExtended.from_orm(region_model)
    region_model.provider.connect(provider_model)
    provider = ProviderReadExtended.from_orm(provider_model)
    assert len(provider.regions) == 1
    assert provider.regions[0] == region
    assert provider.regions[0].location is None
    assert len(provider.regions[0].services) == len(services)


@parametrize_with_cases("services", has_tag="services")
def test_region_read_ext_with_srv_public(
    region_model: Region,
    provider_model: Provider,
    services: list[BlockStorageService]
    | list[ComputeService]
    | list[IdentityService]
    | list[NetworkService]
    | list[ObjectStoreService]
    | list[
        BlockStorageService,
        ComputeService,
        IdentityService,
        NetworkService,
        ObjectStoreService,
    ],
):
    for service in services:
        region_model.services.connect(service)
    region = RegionReadExtendedPublic.from_orm(region_model)
    region_model.provider.connect(provider_model)
    provider = ProviderReadExtendedPublic.from_orm(provider_model)
    assert len(provider.regions) == 1
    assert provider.regions[0] == region
    assert provider.regions[0].location is None
    assert len(provider.regions[0].services) == len(services)


@parametrize_with_cases("quotas", has_tag=("quotas", "block-storage"))
def test_block_storage_serv_read_ext(
    block_storage_service_model: BlockStorageService,
    region_model: Region,
    provider_model: Provider,
    quotas: list[BlockStorageQuota],
):
    for quota in quotas:
        block_storage_service_model.quotas.connect(quota)
    service = BlockStorageServiceReadExtended.from_orm(block_storage_service_model)
    block_storage_service_model.region.connect(region_model)
    region_model.provider.connect(provider_model)
    provider = ProviderReadExtended.from_orm(provider_model)
    assert len(provider.regions[0].services) == 1
    assert provider.regions[0].services[0] == service
    assert len(provider.regions[0].services[0].quotas) == len(quotas)
    assert isinstance(provider.regions[0].services[0].quotas[0], BlockStorageQuotaRead)


@parametrize_with_cases("quotas", has_tag=("quotas", "block-storage"))
def test_block_storage_serv_read_ext_public(
    block_storage_service_model: BlockStorageService,
    region_model: Region,
    provider_model: Provider,
    quotas: list[BlockStorageQuota],
):
    for quota in quotas:
        block_storage_service_model.quotas.connect(quota)
    service = BlockStorageServiceReadExtendedPublic.from_orm(
        block_storage_service_model
    )
    block_storage_service_model.region.connect(region_model)
    region_model.provider.connect(provider_model)
    provider = ProviderReadExtendedPublic.from_orm(provider_model)
    assert len(provider.regions[0].services) == 1
    assert provider.regions[0].services[0] == service
    assert len(provider.regions[0].services[0].quotas) == len(quotas)
    assert isinstance(
        provider.regions[0].services[0].quotas[0], BlockStorageQuotaReadPublic
    )


@parametrize_with_cases("quotas", has_tag=("quotas", "compute"))
def test_compute_serv_read_ext(
    compute_service_model: ComputeService,
    region_model: Region,
    provider_model: Provider,
    quotas: list[ComputeQuota],
):
    for quota in quotas:
        compute_service_model.quotas.connect(quota)
    service = ComputeServiceReadExtended.from_orm(compute_service_model)
    compute_service_model.region.connect(region_model)
    region_model.provider.connect(provider_model)
    provider = ProviderReadExtended.from_orm(provider_model)
    assert len(provider.regions[0].services) == 1
    assert provider.regions[0].services[0] == service
    assert len(provider.regions[0].services[0].quotas) == len(quotas)
    assert isinstance(provider.regions[0].services[0].quotas[0], ComputeQuotaRead)


@parametrize_with_cases("quotas", has_tag=("quotas", "compute"))
def test_compute_serv_read_ext_public(
    compute_service_model: ComputeService,
    region_model: Region,
    provider_model: Provider,
    quotas: list[ComputeQuota],
):
    for quota in quotas:
        compute_service_model.quotas.connect(quota)
    service = ComputeServiceReadExtendedPublic.from_orm(compute_service_model)
    compute_service_model.region.connect(region_model)
    region_model.provider.connect(provider_model)
    provider = ProviderReadExtendedPublic.from_orm(provider_model)
    assert len(provider.regions[0].services) == 1
    assert provider.regions[0].services[0] == service
    assert len(provider.regions[0].services[0].quotas) == len(quotas)
    assert isinstance(provider.regions[0].services[0].quotas[0], ComputeQuotaReadPublic)


@parametrize_with_cases("quotas", has_tag=("quotas", "network"))
def test_network_serv_read_ext(
    network_service_model: NetworkService,
    region_model: Region,
    provider_model: Provider,
    quotas: list[NetworkQuota],
):
    for quota in quotas:
        network_service_model.quotas.connect(quota)
    service = NetworkServiceReadExtended.from_orm(network_service_model)
    network_service_model.region.connect(region_model)
    region_model.provider.connect(provider_model)
    provider = ProviderReadExtended.from_orm(provider_model)
    assert len(provider.regions[0].services) == 1
    assert provider.regions[0].services[0] == service
    assert len(provider.regions[0].services[0].quotas) == len(quotas)
    assert isinstance(provider.regions[0].services[0].quotas[0], NetworkQuotaRead)


@parametrize_with_cases("quotas", has_tag=("quotas", "network"))
def test_network_serv_read_ext_public(
    network_service_model: NetworkService,
    region_model: Region,
    provider_model: Provider,
    quotas: list[NetworkQuota],
):
    for quota in quotas:
        network_service_model.quotas.connect(quota)
    service = NetworkServiceReadExtendedPublic.from_orm(network_service_model)
    network_service_model.region.connect(region_model)
    region_model.provider.connect(provider_model)
    provider = ProviderReadExtendedPublic.from_orm(provider_model)
    assert len(provider.regions[0].services) == 1
    assert provider.regions[0].services[0] == service
    assert len(provider.regions[0].services[0].quotas) == len(quotas)
    assert isinstance(provider.regions[0].services[0].quotas[0], NetworkQuotaReadPublic)


@parametrize_with_cases("quotas", has_tag=("quotas", "object-store"))
def test_object_store_serv_read_ext(
    object_store_service_model: ObjectStoreService,
    region_model: Region,
    provider_model: Provider,
    quotas: list[ObjectStoreQuota],
):
    for quota in quotas:
        object_store_service_model.quotas.connect(quota)
    service = ObjectStoreServiceReadExtended.from_orm(object_store_service_model)
    object_store_service_model.region.connect(region_model)
    region_model.provider.connect(provider_model)
    provider = ProviderReadExtended.from_orm(provider_model)
    assert len(provider.regions[0].services) == 1
    assert provider.regions[0].services[0] == service
    assert len(provider.regions[0].services[0].quotas) == len(quotas)
    assert isinstance(provider.regions[0].services[0].quotas[0], ObjectStoreQuotaRead)


@parametrize_with_cases("quotas", has_tag=("quotas", "object-store"))
def test_object_store_serv_read_ext_public(
    object_store_service_model: ObjectStoreService,
    region_model: Region,
    provider_model: Provider,
    quotas: list[ObjectStoreQuota],
):
    for quota in quotas:
        object_store_service_model.quotas.connect(quota)
    service = ObjectStoreServiceReadExtendedPublic.from_orm(object_store_service_model)
    object_store_service_model.region.connect(region_model)
    region_model.provider.connect(provider_model)
    provider = ProviderReadExtendedPublic.from_orm(provider_model)
    assert len(provider.regions[0].services) == 1
    assert provider.regions[0].services[0] == service
    assert len(provider.regions[0].services[0].quotas) == len(quotas)
    assert isinstance(
        provider.regions[0].services[0].quotas[0], ObjectStoreQuotaReadPublic
    )


@parametrize_with_cases("user_groups", has_tag="user_groups")
def test_identity_provider_read_ext(
    provider_model: Provider,
    identity_provider_model: IdentityProvider,
    user_groups: list[UserGroup],
):
    with pytest.raises(ValidationError):
        IdentityProviderReadExtended.from_orm(identity_provider_model)
    for user_group in user_groups:
        identity_provider_model.user_groups.connect(user_group)
    provider_model.identity_providers.connect(
        identity_provider_model, auth_method_model_dict()
    )
    provider = ProviderReadExtended.from_orm(provider_model)
    assert len(provider.identity_providers) == 1
    assert isinstance(provider.identity_providers[0], IdentityProviderReadExtended)
    assert len(provider.identity_providers[0].user_groups) == len(user_groups)


@parametrize_with_cases("user_groups", has_tag="user_groups")
def test_identity_provider_read_ext_public(
    provider_model: Provider,
    identity_provider_model: IdentityProvider,
    user_groups: list[UserGroup],
):
    with pytest.raises(ValidationError):
        IdentityProviderReadExtendedPublic.from_orm(identity_provider_model)
    for user_group in user_groups:
        identity_provider_model.user_groups.connect(user_group)
    provider_model.identity_providers.connect(
        identity_provider_model, auth_method_model_dict()
    )
    provider = ProviderReadExtendedPublic.from_orm(provider_model)
    assert len(provider.identity_providers) == 1
    assert isinstance(
        provider.identity_providers[0], IdentityProviderReadExtendedPublic
    )
    assert len(provider.identity_providers[0].user_groups) == len(user_groups)


@parametrize_with_cases("slas", has_tag="slas")
def test_user_group_read_ext(
    user_group_model: UserGroup,
    provider_model: Provider,
    identity_provider_model: IdentityProvider,
    slas: list[SLA],
):
    for sla in slas:
        user_group_model.slas.connect(sla)
    user_group = UserGroupReadExtended.from_orm(user_group_model)
    identity_provider_model.user_groups.connect(user_group_model)
    provider_model.identity_providers.connect(
        identity_provider_model, auth_method_model_dict()
    )
    provider = ProviderReadExtended.from_orm(provider_model)
    assert len(provider.identity_providers[0].user_groups) == 1
    assert provider.identity_providers[0].user_groups[0] == user_group
    assert len(provider.identity_providers[0].user_groups[0].slas) == len(slas)
    assert isinstance(provider.identity_providers[0].user_groups[0].slas[0], SLARead)


@parametrize_with_cases("slas", has_tag="slas")
def test_user_group_read_ext_public(
    user_group_model: UserGroup,
    provider_model: Provider,
    identity_provider_model: IdentityProvider,
    slas: list[SLA],
):
    for sla in slas:
        user_group_model.slas.connect(sla)
    user_group = UserGroupReadExtendedPublic.from_orm(user_group_model)
    identity_provider_model.user_groups.connect(user_group_model)
    provider_model.identity_providers.connect(
        identity_provider_model, auth_method_model_dict()
    )
    provider = ProviderReadExtendedPublic.from_orm(provider_model)
    assert len(provider.identity_providers[0].user_groups) == 1
    assert provider.identity_providers[0].user_groups[0] == user_group
    assert len(provider.identity_providers[0].user_groups[0].slas) == len(slas)
    assert isinstance(
        provider.identity_providers[0].user_groups[0].slas[0], SLAReadPublic
    )
