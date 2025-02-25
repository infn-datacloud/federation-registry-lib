import pytest
from neomodel.exceptions import CardinalityViolation
from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from fedreg.auth_method.schemas import AuthMethodRead
from fedreg.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.flavor.models import PrivateFlavor, SharedFlavor
from fedreg.identity_provider.models import IdentityProvider
from fedreg.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from fedreg.image.models import PrivateImage, SharedImage
from fedreg.network.models import PrivateNetwork, SharedNetwork
from fedreg.network.schemas import NetworkRead, NetworkReadPublic
from fedreg.project.models import Project
from fedreg.project.schemas import ProjectRead, ProjectReadPublic
from fedreg.project.schemas_extended import (
    BlockStorageQuotaReadExtended,
    BlockStorageQuotaReadExtendedPublic,
    BlockStorageServiceReadExtended,
    BlockStorageServiceReadExtendedPublic,
    ComputeQuotaReadExtended,
    ComputeQuotaReadExtendedPublic,
    ComputeServiceReadExtended,
    ComputeServiceReadExtendedPublic,
    IdentityProviderReadExtended,
    IdentityProviderReadExtendedPublic,
    NetworkQuotaReadExtended,
    NetworkQuotaReadExtendedPublic,
    NetworkReadExtended,
    NetworkReadExtendedPublic,
    NetworkServiceReadExtended,
    NetworkServiceReadExtendedPublic,
    ObjectStoreQuotaReadExtended,
    ObjectStoreQuotaReadExtendedPublic,
    ObjectStoreServiceReadExtended,
    ObjectStoreServiceReadExtendedPublic,
    ProjectReadExtended,
    ProjectReadExtendedPublic,
    ProviderReadExtended,
    ProviderReadExtendedPublic,
    ProviderReadWithAuthMethod,
    RegionReadExtended,
    RegionReadExtendedPublic,
    SLAReadExtended,
    SLAReadExtendedPublic,
    UserGroupReadExtended,
    UserGroupReadExtendedPublic,
)
from fedreg.provider.models import Provider
from fedreg.provider.schemas import ProviderRead, ProviderReadPublic
from fedreg.quota.models import (
    BlockStorageQuota,
    ComputeQuota,
    NetworkQuota,
    ObjectStoreQuota,
)
from fedreg.quota.schemas import (
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    NetworkQuotaRead,
    NetworkQuotaReadPublic,
    ObjectStoreQuotaRead,
    ObjectStoreQuotaReadPublic,
)
from fedreg.region.models import Region
from fedreg.region.schemas import RegionRead, RegionReadPublic
from fedreg.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
    ObjectStoreService,
)
from fedreg.service.schemas import (
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    IdentityServiceReadPublic,
    NetworkServiceRead,
    NetworkServiceReadPublic,
    ObjectStoreServiceRead,
    ObjectStoreServiceReadPublic,
)
from fedreg.sla.models import SLA
from fedreg.sla.schemas import SLARead, SLAReadPublic
from fedreg.user_group.models import UserGroup
from fedreg.user_group.schemas import UserGroupRead, UserGroupReadPublic
from tests.models.utils import auth_method_model_dict


def test_class_inheritance():
    assert issubclass(ProjectReadExtended, BaseReadPrivateExtended)
    assert issubclass(ProjectReadExtended, ProjectRead)
    assert ProjectReadExtended.__fields__["schema_type"].default == "private_extended"
    assert ProjectReadExtended.__config__.orm_mode is True

    assert issubclass(ProjectReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(ProjectReadExtendedPublic, ProjectReadPublic)
    assert (
        ProjectReadExtendedPublic.__fields__["schema_type"].default == "public_extended"
    )
    assert ProjectReadExtendedPublic.__config__.orm_mode is True

    assert issubclass(ProviderReadExtended, ProviderRead)
    assert issubclass(ProviderReadExtendedPublic, ProviderReadPublic)

    assert issubclass(RegionReadExtended, RegionRead)
    assert issubclass(RegionReadExtendedPublic, RegionReadPublic)

    assert issubclass(SLAReadExtended, SLARead)
    assert issubclass(SLAReadExtendedPublic, SLAReadPublic)

    assert issubclass(UserGroupReadExtended, UserGroupRead)
    assert issubclass(UserGroupReadExtendedPublic, UserGroupReadPublic)

    assert issubclass(IdentityProviderReadExtended, IdentityProviderRead)
    assert issubclass(IdentityProviderReadExtendedPublic, IdentityProviderReadPublic)

    assert issubclass(BlockStorageQuotaReadExtended, BlockStorageQuotaRead)
    assert issubclass(BlockStorageQuotaReadExtendedPublic, BlockStorageQuotaReadPublic)

    assert issubclass(ComputeQuotaReadExtended, ComputeQuotaRead)
    assert issubclass(ComputeQuotaReadExtendedPublic, ComputeQuotaReadPublic)

    assert issubclass(NetworkQuotaReadExtended, NetworkQuotaRead)
    assert issubclass(NetworkQuotaReadExtendedPublic, NetworkQuotaReadPublic)

    assert issubclass(ObjectStoreQuotaReadExtended, ObjectStoreQuotaRead)
    assert issubclass(ObjectStoreQuotaReadExtendedPublic, ObjectStoreQuotaReadPublic)

    assert issubclass(NetworkReadExtended, NetworkRead)
    assert issubclass(NetworkReadExtendedPublic, NetworkReadPublic)

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

    assert issubclass(ProviderReadWithAuthMethod, ProviderReadPublic)


@parametrize_with_cases("sla", has_tag="sla")
def test_read_ext(
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    sla: SLA | None,
) -> None:
    provider_model.regions.connect(region_model)
    project_model.provider.connect(provider_model)
    if sla is not None:
        project_model.sla.connect(sla)

    item = ProjectReadExtendedPublic.from_orm(project_model)
    assert item.provider is not None
    assert item.provider == ProviderReadExtendedPublic.from_orm(provider_model)
    if sla is None:
        assert item.sla is None
    else:
        assert item.sla == SLAReadExtendedPublic.from_orm(sla)
    assert len(item.flavors) == 0
    assert len(item.images) == 0
    assert len(item.networks) == 0
    assert len(item.quotas) == 0

    item = ProjectReadExtended.from_orm(project_model)
    assert item.provider is not None
    assert item.provider == ProviderReadExtended.from_orm(provider_model)
    if sla is None:
        assert item.sla is None
    else:
        assert item.sla == SLAReadExtended.from_orm(sla)
    assert len(item.flavors) == 0
    assert len(item.images) == 0
    assert len(item.networks) == 0
    assert len(item.quotas) == 0


@parametrize_with_cases("private_flavors, shared_flavors", has_tag="flavors")
def test_read_flavors(
    project_model: Project,
    provider_model: Provider,
    compute_quota_model: ComputeQuota,
    private_flavors: list[PrivateFlavor],
    shared_flavors: list[SharedFlavor],
) -> None:
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(compute_quota_model)
    for flavor in private_flavors:
        project_model.private_flavors.connect(flavor)

    item = ProjectReadExtendedPublic.from_orm(project_model)
    assert item.provider is not None
    assert item.provider == ProviderReadExtendedPublic.from_orm(provider_model)
    assert item.sla is None
    assert len(item.flavors) == len(private_flavors) + len(shared_flavors)
    assert len(item.images) == 0
    assert len(item.networks) == 0
    assert len(item.quotas) == 1

    item = ProjectReadExtended.from_orm(project_model)
    assert item.provider is not None
    assert item.provider == ProviderReadExtended.from_orm(provider_model)
    assert item.sla is None
    assert len(item.flavors) == len(private_flavors) + len(shared_flavors)
    assert len(item.images) == 0
    assert len(item.networks) == 0
    assert len(item.quotas) == 1


@parametrize_with_cases("private_images, shared_images", has_tag="images")
def test_read_images(
    project_model: Project,
    provider_model: Provider,
    compute_quota_model: ComputeQuota,
    private_images: list[PrivateImage],
    shared_images: list[SharedImage],
) -> None:
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(compute_quota_model)
    for image in private_images:
        project_model.private_images.connect(image)

    item = ProjectReadExtendedPublic.from_orm(project_model)
    assert item.provider is not None
    assert item.provider == ProviderReadExtendedPublic.from_orm(provider_model)
    assert item.sla is None
    assert len(item.flavors) == 0
    assert len(item.images) == len(private_images) + len(shared_images)
    assert len(item.networks) == 0
    assert len(item.quotas) == 1

    item = ProjectReadExtended.from_orm(project_model)
    assert item.provider is not None
    assert item.provider == ProviderReadExtended.from_orm(provider_model)
    assert item.sla is None
    assert len(item.flavors) == 0
    assert len(item.images) == len(private_images) + len(shared_images)
    assert len(item.networks) == 0
    assert len(item.quotas) == 1


@parametrize_with_cases("private_networks, shared_networks", has_tag="networks")
def test_read_networks(
    project_model: Project,
    provider_model: Provider,
    network_quota_model: NetworkQuota,
    private_networks: list[PrivateNetwork],
    shared_networks: list[SharedNetwork],
) -> None:
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(network_quota_model)
    for network in private_networks:
        project_model.private_networks.connect(network)

    item = ProjectReadExtendedPublic.from_orm(project_model)
    assert item.provider is not None
    assert item.provider == ProviderReadExtendedPublic.from_orm(provider_model)
    assert item.sla is None
    assert len(item.flavors) == 0
    assert len(item.images) == 0
    assert len(item.networks) == len(private_networks) + len(shared_networks)
    assert len(item.quotas) == 1

    item = ProjectReadExtended.from_orm(project_model)
    assert item.provider is not None
    assert item.provider == ProviderReadExtended.from_orm(provider_model)
    assert item.sla is None
    assert len(item.flavors) == 0
    assert len(item.images) == 0
    assert len(item.networks) == len(private_networks) + len(shared_networks)
    assert len(item.quotas) == 1


@parametrize_with_cases("quotas", has_tag="quotas")
def test_read_quotas(
    project_model: Project,
    provider_model: Provider,
    quotas: list[BlockStorageQuota]
    | list[ComputeQuota]
    | list[NetworkQuota]
    | list[ObjectStoreQuota]
    | list[BlockStorageQuota | ComputeQuota | NetworkQuota | ObjectStoreQuota],
) -> None:
    project_model.provider.connect(provider_model)
    for quota in quotas:
        project_model.quotas.connect(quota)

    item = ProjectReadExtendedPublic.from_orm(project_model)
    assert item.provider is not None
    assert item.provider == ProviderReadExtendedPublic.from_orm(provider_model)
    assert item.sla is None
    assert len(item.flavors) == 0
    assert len(item.images) == 0
    assert len(item.networks) == 0
    assert len(item.quotas) == len(quotas)

    item = ProjectReadExtended.from_orm(project_model)
    assert item.provider is not None
    assert item.provider == ProviderReadExtended.from_orm(provider_model)
    assert item.sla is None
    assert len(item.flavors) == 0
    assert len(item.images) == 0
    assert len(item.networks) == 0
    assert len(item.quotas) == len(quotas)


def test_sla_read_ext(
    sla_model: SLA,
    user_group_model: UserGroup,
    provider_model: Provider,
    identity_provider_model: IdentityProvider,
    project_model: Project,
):
    with pytest.raises(CardinalityViolation):
        SLAReadExtended.from_orm(sla_model)
    provider_model.identity_providers.connect(
        identity_provider_model, auth_method_model_dict()
    )
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla = SLAReadExtended.from_orm(sla_model)
    project_model.provider.connect(provider_model)
    project_model.sla.connect(sla_model)
    project = ProjectReadExtended.from_orm(project_model)
    assert project.sla == sla


def test_sla_read_ext_public(
    sla_model: SLA,
    user_group_model: UserGroup,
    provider_model: Provider,
    identity_provider_model: IdentityProvider,
    project_model: Project,
):
    with pytest.raises(CardinalityViolation):
        SLAReadExtendedPublic.from_orm(sla_model)
    provider_model.identity_providers.connect(
        identity_provider_model, auth_method_model_dict()
    )
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla = SLAReadExtendedPublic.from_orm(sla_model)
    project_model.provider.connect(provider_model)
    project_model.sla.connect(sla_model)
    project = ProjectReadExtendedPublic.from_orm(project_model)
    assert project.sla == sla


def test_user_group_read_ext(
    sla_model: SLA,
    user_group_model: UserGroup,
    provider_model: Provider,
    identity_provider_model: IdentityProvider,
    project_model: Project,
):
    with pytest.raises(CardinalityViolation):
        UserGroupReadExtended.from_orm(user_group_model)
    provider_model.identity_providers.connect(
        identity_provider_model, auth_method_model_dict()
    )
    identity_provider_model.user_groups.connect(user_group_model)
    user_group = UserGroupReadExtended.from_orm(user_group_model)
    user_group_model.slas.connect(sla_model)
    project_model.provider.connect(provider_model)
    project_model.sla.connect(sla_model)
    project = ProjectReadExtended.from_orm(project_model)
    assert project.sla.user_group == user_group


def test_user_group_read_ext_public(
    sla_model: SLA,
    user_group_model: UserGroup,
    provider_model: Provider,
    identity_provider_model: IdentityProvider,
    project_model: Project,
):
    with pytest.raises(CardinalityViolation):
        UserGroupReadExtendedPublic.from_orm(user_group_model)
    provider_model.identity_providers.connect(
        identity_provider_model, auth_method_model_dict()
    )
    identity_provider_model.user_groups.connect(user_group_model)
    user_group = UserGroupReadExtendedPublic.from_orm(user_group_model)
    user_group_model.slas.connect(sla_model)
    project_model.provider.connect(provider_model)
    project_model.sla.connect(sla_model)
    project = ProjectReadExtendedPublic.from_orm(project_model)
    assert project.sla.user_group == user_group


@parametrize_with_cases("providers", has_tag="providers")
def test_identity_provider_read_ext(
    sla_model: SLA,
    user_group_model: UserGroup,
    identity_provider_model: IdentityProvider,
    project_model: Project,
    providers: list[Provider],
):
    with pytest.raises(CardinalityViolation):
        IdentityProviderReadExtended.from_orm(identity_provider_model)
    for provider in providers:
        provider.identity_providers.connect(
            identity_provider_model, auth_method_model_dict()
        )
    identity_provider = IdentityProviderReadExtended.from_orm(identity_provider_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    project_model.sla.connect(sla_model)
    # Connect the project to only one provider (the last one)
    project_model.provider.connect(provider)
    project = ProjectReadExtended.from_orm(project_model)
    assert project.sla.user_group.identity_provider == identity_provider
    assert len(project.sla.user_group.identity_provider.providers) == len(providers)


@parametrize_with_cases("providers", has_tag="providers")
def test_identity_provider_read_ext_public(
    sla_model: SLA,
    user_group_model: UserGroup,
    identity_provider_model: IdentityProvider,
    project_model: Project,
    providers: list[Provider],
):
    with pytest.raises(CardinalityViolation):
        IdentityProviderReadExtendedPublic.from_orm(identity_provider_model)
    for provider in providers:
        provider.identity_providers.connect(
            identity_provider_model, auth_method_model_dict()
        )
    identity_provider = IdentityProviderReadExtendedPublic.from_orm(
        identity_provider_model
    )
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    project_model.sla.connect(sla_model)
    # Connect the project to only one provider (the last one)
    project_model.provider.connect(provider)
    project = ProjectReadExtendedPublic.from_orm(project_model)
    assert project.sla.user_group.identity_provider == identity_provider
    assert len(project.sla.user_group.identity_provider.providers) == len(providers)


def test_provider_with_auth_method(
    sla_model: SLA,
    user_group_model: UserGroup,
    identity_provider_model: IdentityProvider,
    project_model: Project,
    provider_model: Provider,
):
    with pytest.raises(ValidationError):
        ProviderReadWithAuthMethod.from_orm(provider_model)
    auth_method = auth_method_model_dict()
    provider_model.identity_providers.connect(identity_provider_model, auth_method)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    project_model.sla.connect(sla_model)
    project_model.provider.connect(provider_model)
    project = ProjectReadExtended.from_orm(project_model)
    assert len(project.sla.user_group.identity_provider.providers) == 1
    assert isinstance(
        project.sla.user_group.identity_provider.providers[0],
        ProviderReadWithAuthMethod,
    )
    assert project.sla.user_group.identity_provider.providers[
        0
    ].relationship == AuthMethodRead(**auth_method)


@parametrize_with_cases("network", has_tag="network_kind")
def test_network_read_ext(
    region_model: Region,
    provider_model: Provider,
    network_service_model: NetworkService,
    network_quota_model: NetworkQuota,
    project_model: Project,
    network: PrivateNetwork | SharedNetwork,
):
    with pytest.raises(CardinalityViolation):
        NetworkReadExtended.from_orm(network)
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    network_service_model.networks.connect(network)
    if isinstance(network, PrivateNetwork):
        project_model.private_networks.connect(network)
    item = NetworkReadExtended.from_orm(network)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(network_quota_model)
    network_quota_model.service.connect(network_service_model)
    project = ProjectReadExtended.from_orm(project_model)
    assert len(project.networks) == 1
    assert project.networks[0] == item
    assert isinstance(project.networks[0].service, NetworkServiceRead)


@parametrize_with_cases("network", has_tag="network_kind")
def test_network_read_ext_public(
    region_model: Region,
    provider_model: Provider,
    network_service_model: NetworkService,
    network_quota_model: NetworkQuota,
    project_model: Project,
    network: PrivateNetwork | SharedNetwork,
):
    with pytest.raises(CardinalityViolation):
        NetworkReadExtendedPublic.from_orm(network)
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    network_service_model.networks.connect(network)
    if isinstance(network, PrivateNetwork):
        project_model.private_networks.connect(network)
    item = NetworkReadExtendedPublic.from_orm(network)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(network_quota_model)
    network_quota_model.service.connect(network_service_model)
    project = ProjectReadExtendedPublic.from_orm(project_model)
    assert len(project.networks) == 1
    assert project.networks[0] == item
    assert isinstance(project.networks[0].service, NetworkServiceReadPublic)


@parametrize_with_cases("regions", has_tag="regions")
def test_provider_read_ext(
    provider_model: Provider, project_model: Project, regions: list[Region]
):
    for region in regions:
        provider_model.regions.connect(region)
    provider = ProviderReadExtended.from_orm(provider_model)
    project_model.provider.connect(provider_model)
    project = ProjectReadExtended.from_orm(project_model)
    assert project.provider == provider
    assert len(project.provider.regions) == len(regions)


@parametrize_with_cases("regions", has_tag="regions")
def test_provider_read_ext_public(
    provider_model: Provider, project_model: Project, regions: list[Region]
):
    for region in regions:
        provider_model.regions.connect(region)
    provider = ProviderReadExtendedPublic.from_orm(provider_model)
    project_model.provider.connect(provider_model)
    project = ProjectReadExtendedPublic.from_orm(project_model)
    assert project.provider == provider
    assert len(project.provider.regions) == len(regions)


@parametrize_with_cases("identity_services", has_tag="id_srv")
def test_region_read_ext(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    block_storage_service_model: BlockStorageService,
    compute_service_model: ComputeService,
    network_service_model: NetworkService,
    object_store_service_model: ObjectStoreService,
    identity_services: list[IdentityService],
):
    for service in identity_services:
        region_model.services.connect(service)
    region_model.services.connect(block_storage_service_model)
    region_model.services.connect(compute_service_model)
    region_model.services.connect(network_service_model)
    region_model.services.connect(object_store_service_model)
    region = RegionReadExtended.from_orm(region_model)
    region_model.provider.connect(provider_model)
    project_model.provider.connect(provider_model)
    project = ProjectReadExtended.from_orm(project_model)
    assert len(project.provider.regions) == 1
    assert project.provider.regions[0] == region
    # Ignore not 'identity' services
    assert len(project.provider.regions[0].identity_services) == len(identity_services)
    if len(project.provider.regions[0].identity_services) > 0:
        assert isinstance(
            project.provider.regions[0].identity_services[0], IdentityServiceReadPublic
        )


@parametrize_with_cases("identity_services", has_tag="id_srv")
def test_region_read_ext_public(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    block_storage_service_model: BlockStorageService,
    compute_service_model: ComputeService,
    network_service_model: NetworkService,
    object_store_service_model: ObjectStoreService,
    identity_services: list[IdentityService],
):
    for service in identity_services:
        region_model.services.connect(service)
    region_model.services.connect(block_storage_service_model)
    region_model.services.connect(compute_service_model)
    region_model.services.connect(network_service_model)
    region_model.services.connect(object_store_service_model)
    region = RegionReadExtendedPublic.from_orm(region_model)
    region_model.provider.connect(provider_model)
    project_model.provider.connect(provider_model)
    project = ProjectReadExtendedPublic.from_orm(project_model)
    assert len(project.provider.regions) == 1
    assert project.provider.regions[0] == region
    # Ignore not 'identity' services
    assert len(project.provider.regions[0].identity_services) == len(identity_services)
    if len(project.provider.regions[0].identity_services) > 0:
        assert isinstance(
            project.provider.regions[0].identity_services[0], IdentityServiceReadPublic
        )


def test_block_storage_quota_read_ext(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    block_storage_quota_model: BlockStorageQuota,
    block_storage_service_model: BlockStorageService,
):
    with pytest.raises(CardinalityViolation):
        BlockStorageQuotaReadExtended.from_orm(block_storage_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(block_storage_service_model)
    block_storage_service_model.quotas.connect(block_storage_quota_model)
    quota = BlockStorageQuotaReadExtended.from_orm(block_storage_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(block_storage_quota_model)
    project = ProjectReadExtended.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0] == quota


def test_block_storage_quota_read_ext_public(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    block_storage_quota_model: BlockStorageQuota,
    block_storage_service_model: BlockStorageService,
):
    with pytest.raises(CardinalityViolation):
        BlockStorageQuotaReadExtendedPublic.from_orm(block_storage_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(block_storage_service_model)
    block_storage_service_model.quotas.connect(block_storage_quota_model)
    quota = BlockStorageQuotaReadExtendedPublic.from_orm(block_storage_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(block_storage_quota_model)
    project = ProjectReadExtendedPublic.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0] == quota


def test_compute_quota_read_ext(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    compute_quota_model: ComputeQuota,
    compute_service_model: ComputeService,
):
    with pytest.raises(CardinalityViolation):
        ComputeQuotaReadExtended.from_orm(compute_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    compute_service_model.quotas.connect(compute_quota_model)
    quota = ComputeQuotaReadExtended.from_orm(compute_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(compute_quota_model)
    project = ProjectReadExtended.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0] == quota


def test_compute_quota_read_ext_public(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    compute_quota_model: ComputeQuota,
    compute_service_model: ComputeService,
):
    with pytest.raises(CardinalityViolation):
        ComputeQuotaReadExtendedPublic.from_orm(compute_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    compute_service_model.quotas.connect(compute_quota_model)
    quota = ComputeQuotaReadExtendedPublic.from_orm(compute_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(compute_quota_model)
    project = ProjectReadExtendedPublic.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0] == quota


def test_network_quota_read_ext(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    network_quota_model: NetworkQuota,
    network_service_model: NetworkService,
):
    with pytest.raises(CardinalityViolation):
        NetworkQuotaReadExtended.from_orm(network_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    network_service_model.quotas.connect(network_quota_model)
    quota = NetworkQuotaReadExtended.from_orm(network_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(network_quota_model)
    project = ProjectReadExtended.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0] == quota


def test_network_quota_read_ext_public(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    network_quota_model: NetworkQuota,
    network_service_model: NetworkService,
):
    with pytest.raises(CardinalityViolation):
        NetworkQuotaReadExtendedPublic.from_orm(network_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    network_service_model.quotas.connect(network_quota_model)
    quota = NetworkQuotaReadExtendedPublic.from_orm(network_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(network_quota_model)
    project = ProjectReadExtendedPublic.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0] == quota


def test_object_store_quota_read_ext(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    object_store_quota_model: ObjectStoreQuota,
    object_store_service_model: ObjectStoreService,
):
    with pytest.raises(CardinalityViolation):
        ObjectStoreQuotaReadExtended.from_orm(object_store_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(object_store_service_model)
    object_store_service_model.quotas.connect(object_store_quota_model)
    quota = ObjectStoreQuotaReadExtended.from_orm(object_store_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(object_store_quota_model)
    project = ProjectReadExtended.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0] == quota


def test_object_store_quota_read_ext_public(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    object_store_quota_model: ObjectStoreQuota,
    object_store_service_model: ObjectStoreService,
):
    with pytest.raises(CardinalityViolation):
        ObjectStoreQuotaReadExtendedPublic.from_orm(object_store_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(object_store_service_model)
    object_store_service_model.quotas.connect(object_store_quota_model)
    quota = ObjectStoreQuotaReadExtendedPublic.from_orm(object_store_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(object_store_quota_model)
    project = ProjectReadExtendedPublic.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0] == quota


def test_block_storage_service_read_ext(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    block_storage_quota_model: BlockStorageQuota,
    block_storage_service_model: BlockStorageService,
):
    with pytest.raises(CardinalityViolation):
        BlockStorageServiceReadExtended.from_orm(block_storage_service_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(block_storage_service_model)
    service = BlockStorageServiceReadExtended.from_orm(block_storage_service_model)
    block_storage_service_model.quotas.connect(block_storage_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(block_storage_quota_model)
    project = ProjectReadExtended.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0].service == service
    assert isinstance(project.quotas[0].service.region, RegionReadPublic)


def test_block_storage_service_read_ext_public(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    block_storage_quota_model: BlockStorageQuota,
    block_storage_service_model: BlockStorageService,
):
    with pytest.raises(CardinalityViolation):
        BlockStorageServiceReadExtendedPublic.from_orm(block_storage_service_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(block_storage_service_model)
    service = BlockStorageServiceReadExtendedPublic.from_orm(
        block_storage_service_model
    )
    block_storage_service_model.quotas.connect(block_storage_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(block_storage_quota_model)
    project = ProjectReadExtendedPublic.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0].service == service
    assert isinstance(project.quotas[0].service.region, RegionReadPublic)


def test_compute_service_read_ext(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    compute_quota_model: ComputeQuota,
    compute_service_model: ComputeService,
):
    with pytest.raises(CardinalityViolation):
        ComputeServiceReadExtended.from_orm(compute_service_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    service = ComputeServiceReadExtended.from_orm(compute_service_model)
    compute_service_model.quotas.connect(compute_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(compute_quota_model)
    project = ProjectReadExtended.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0].service == service
    assert isinstance(project.quotas[0].service.region, RegionReadPublic)


def test_compute_service_read_ext_public(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    compute_quota_model: ComputeQuota,
    compute_service_model: ComputeService,
):
    with pytest.raises(CardinalityViolation):
        ComputeServiceReadExtendedPublic.from_orm(compute_service_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    service = ComputeServiceReadExtendedPublic.from_orm(compute_service_model)
    compute_service_model.quotas.connect(compute_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(compute_quota_model)
    project = ProjectReadExtendedPublic.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0].service == service
    assert isinstance(project.quotas[0].service.region, RegionReadPublic)


def test_network_service_read_ext(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    network_quota_model: NetworkQuota,
    network_service_model: NetworkService,
):
    with pytest.raises(CardinalityViolation):
        NetworkServiceReadExtended.from_orm(network_service_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    service = NetworkServiceReadExtended.from_orm(network_service_model)
    network_service_model.quotas.connect(network_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(network_quota_model)
    project = ProjectReadExtended.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0].service == service
    assert isinstance(project.quotas[0].service.region, RegionReadPublic)


def test_network_service_read_ext_public(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    network_quota_model: NetworkQuota,
    network_service_model: NetworkService,
):
    with pytest.raises(CardinalityViolation):
        NetworkServiceReadExtendedPublic.from_orm(network_service_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    service = NetworkServiceReadExtendedPublic.from_orm(network_service_model)
    network_service_model.quotas.connect(network_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(network_quota_model)
    project = ProjectReadExtendedPublic.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0].service == service
    assert isinstance(project.quotas[0].service.region, RegionReadPublic)


def test_object_store_service_read_ext(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    object_store_quota_model: ObjectStoreQuota,
    object_store_service_model: ObjectStoreService,
):
    with pytest.raises(CardinalityViolation):
        ObjectStoreServiceReadExtended.from_orm(object_store_service_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(object_store_service_model)
    service = ObjectStoreServiceReadExtended.from_orm(object_store_service_model)
    object_store_service_model.quotas.connect(object_store_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(object_store_quota_model)
    project = ProjectReadExtended.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0].service == service
    assert isinstance(project.quotas[0].service.region, RegionReadPublic)


def test_object_store_service_read_ext_public(
    provider_model: Provider,
    region_model: Region,
    project_model: Project,
    object_store_quota_model: ObjectStoreQuota,
    object_store_service_model: ObjectStoreService,
):
    with pytest.raises(CardinalityViolation):
        ObjectStoreServiceReadExtendedPublic.from_orm(object_store_service_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(object_store_service_model)
    service = ObjectStoreServiceReadExtendedPublic.from_orm(object_store_service_model)
    object_store_service_model.quotas.connect(object_store_quota_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(object_store_quota_model)
    project = ProjectReadExtendedPublic.from_orm(project_model)
    assert len(project.quotas) == 1
    assert project.quotas[0].service == service
    assert isinstance(project.quotas[0].service.region, RegionReadPublic)
