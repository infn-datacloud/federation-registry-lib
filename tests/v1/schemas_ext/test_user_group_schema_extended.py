import pytest
from neomodel.exceptions import CardinalityViolation
from pytest_cases import parametrize_with_cases

from fedreg.v1.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.v1.identity_provider.models import IdentityProvider
from fedreg.v1.identity_provider.schemas import (
    IdentityProviderRead,
    IdentityProviderReadPublic,
)
from fedreg.v1.project.models import Project
from fedreg.v1.project.schemas import ProjectRead, ProjectReadPublic
from fedreg.v1.provider.models import Provider
from fedreg.v1.provider.schemas import ProviderRead, ProviderReadPublic
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
from fedreg.v1.region.schemas import RegionReadPublic
from fedreg.v1.service.models import (
    BlockStorageService,
    ComputeService,
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
from fedreg.v1.user_group.schemas_extended import (
    BlockStorageQuotaReadExtended,
    BlockStorageQuotaReadExtendedPublic,
    BlockStorageServiceReadExtended,
    BlockStorageServiceReadExtendedPublic,
    ComputeQuotaReadExtended,
    ComputeQuotaReadExtendedPublic,
    ComputeServiceReadExtended,
    ComputeServiceReadExtendedPublic,
    NetworkQuotaReadExtended,
    NetworkQuotaReadExtendedPublic,
    NetworkServiceReadExtended,
    NetworkServiceReadExtendedPublic,
    ObjectStoreQuotaReadExtended,
    ObjectStoreQuotaReadExtendedPublic,
    ObjectStoreServiceReadExtended,
    ObjectStoreServiceReadExtendedPublic,
    ProjectReadExtended,
    ProjectReadExtendedPublic,
    SLAReadExtended,
    SLAReadExtendedPublic,
    UserGroupReadExtended,
    UserGroupReadExtendedPublic,
)


def test_class_inheritance():
    assert issubclass(UserGroupReadExtended, BaseReadPrivateExtended)
    assert issubclass(UserGroupReadExtended, UserGroupRead)
    assert UserGroupReadExtended.__fields__["schema_type"].default == "private_extended"
    assert UserGroupReadExtended.__config__.orm_mode is True

    assert issubclass(UserGroupReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(UserGroupReadExtendedPublic, UserGroupReadPublic)
    assert (
        UserGroupReadExtendedPublic.__fields__["schema_type"].default
        == "public_extended"
    )
    assert UserGroupReadExtendedPublic.__config__.orm_mode is True

    assert issubclass(SLAReadExtended, SLARead)
    assert issubclass(SLAReadExtendedPublic, SLAReadPublic)

    assert issubclass(ProjectReadExtended, ProjectRead)
    assert issubclass(ProjectReadExtendedPublic, ProjectReadPublic)

    assert issubclass(BlockStorageQuotaReadExtended, BlockStorageQuotaRead)
    assert issubclass(BlockStorageQuotaReadExtendedPublic, BlockStorageQuotaReadPublic)

    assert issubclass(ComputeQuotaReadExtended, ComputeQuotaRead)
    assert issubclass(ComputeQuotaReadExtendedPublic, ComputeQuotaReadPublic)

    assert issubclass(NetworkQuotaReadExtended, NetworkQuotaRead)
    assert issubclass(NetworkQuotaReadExtendedPublic, NetworkQuotaReadPublic)

    assert issubclass(ObjectStoreQuotaReadExtended, ObjectStoreQuotaRead)
    assert issubclass(ObjectStoreQuotaReadExtendedPublic, ObjectStoreQuotaReadPublic)

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


@parametrize_with_cases("slas", has_tag="slas")
def test_read_ext(
    user_group_model: UserGroup,
    identity_provider_model: IdentityProvider,
    slas: list[SLA],
) -> None:
    user_group_model.identity_provider.connect(identity_provider_model)
    for sla in slas:
        user_group_model.slas.connect(sla)

    item = UserGroupReadExtendedPublic.from_orm(user_group_model)
    assert item.identity_provider == IdentityProviderReadPublic.from_orm(
        identity_provider_model
    )
    assert len(item.slas) == len(slas)

    item = UserGroupReadExtended.from_orm(user_group_model)
    assert item.identity_provider == IdentityProviderRead.from_orm(
        identity_provider_model
    )
    assert len(item.slas) == len(slas)


@parametrize_with_cases("projects", has_tag="projects")
def test_sla_read_ext(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    projects: list[Project],
):
    with pytest.raises(CardinalityViolation):
        SLAReadExtended.from_orm(sla_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    for project in projects:
        sla_model.projects.connect(project)
    user_group = UserGroupReadExtended.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert user_group.slas[0] == SLAReadExtended.from_orm(sla_model)
    assert len(user_group.slas[0].projects) == len(projects)


@parametrize_with_cases("projects", has_tag="projects")
def test_sla_read_ext_public(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    projects: list[Project],
):
    with pytest.raises(CardinalityViolation):
        SLAReadExtendedPublic.from_orm(sla_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    for project in projects:
        sla_model.projects.connect(project)
    user_group = UserGroupReadExtendedPublic.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert user_group.slas[0] == SLAReadExtendedPublic.from_orm(sla_model)
    assert len(user_group.slas[0].projects) == len(projects)


@parametrize_with_cases("quotas", has_tag="quotas")
def test_project_read_ext(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    quotas: list[BlockStorageQuota]
    | list[ComputeQuota]
    | list[NetworkQuota]
    | list[ObjectStoreQuota]
    | list[BlockStorageQuota | ComputeQuota | NetworkQuota | ObjectStoreQuota],
):
    with pytest.raises(CardinalityViolation):
        ProjectReadExtended.from_orm(project_model)
    project_model.provider.connect(provider_model)
    for quota in quotas:
        project_model.quotas.connect(quota)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    user_group = UserGroupReadExtended.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert user_group.slas[0].projects[0] == ProjectReadExtended.from_orm(project_model)
    assert user_group.slas[0].projects[0].provider == ProviderRead.from_orm(
        provider_model
    )
    assert len(user_group.slas[0].projects[0].quotas) == len(quotas)


@parametrize_with_cases("quotas", has_tag="quotas")
def test_project_read_ext_public(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    quotas: list[BlockStorageQuota]
    | list[ComputeQuota]
    | list[NetworkQuota]
    | list[ObjectStoreQuota]
    | list[BlockStorageQuota | ComputeQuota | NetworkQuota | ObjectStoreQuota],
):
    with pytest.raises(CardinalityViolation):
        ProjectReadExtendedPublic.from_orm(project_model)
    project_model.provider.connect(provider_model)
    for quota in quotas:
        project_model.quotas.connect(quota)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    user_group = UserGroupReadExtendedPublic.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert user_group.slas[0].projects[0] == ProjectReadExtendedPublic.from_orm(
        project_model
    )
    assert user_group.slas[0].projects[0].provider == ProviderReadPublic.from_orm(
        provider_model
    )
    assert len(user_group.slas[0].projects[0].quotas) == len(quotas)


def test_block_storage_quota_read_ext(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    block_storage_quota_model: BlockStorageQuota,
    block_storage_service_model: BlockStorageService,
):
    with pytest.raises(CardinalityViolation):
        BlockStorageQuotaReadExtended.from_orm(block_storage_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(block_storage_service_model)
    block_storage_quota_model.service.connect(block_storage_service_model)
    quota = BlockStorageQuotaReadExtended.from_orm(block_storage_quota_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(block_storage_quota_model)
    user_group = UserGroupReadExtended.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0] == quota


def test_block_storage_quota_read_ext_public(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    block_storage_quota_model: BlockStorageQuota,
    block_storage_service_model: BlockStorageService,
):
    with pytest.raises(CardinalityViolation):
        BlockStorageQuotaReadExtendedPublic.from_orm(block_storage_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(block_storage_service_model)
    block_storage_quota_model.service.connect(block_storage_service_model)
    quota = BlockStorageQuotaReadExtendedPublic.from_orm(block_storage_quota_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(block_storage_quota_model)
    user_group = UserGroupReadExtendedPublic.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0] == quota


def test_compute_quota_read_ext(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    compute_quota_model: ComputeQuota,
    compute_service_model: ComputeService,
):
    with pytest.raises(CardinalityViolation):
        ComputeQuotaReadExtended.from_orm(compute_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    compute_quota_model.service.connect(compute_service_model)
    quota = ComputeQuotaReadExtended.from_orm(compute_quota_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(compute_quota_model)
    user_group = UserGroupReadExtended.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0] == quota


def test_compute_quota_read_ext_public(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    compute_quota_model: ComputeQuota,
    compute_service_model: ComputeService,
):
    with pytest.raises(CardinalityViolation):
        ComputeQuotaReadExtendedPublic.from_orm(compute_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    compute_quota_model.service.connect(compute_service_model)
    quota = ComputeQuotaReadExtendedPublic.from_orm(compute_quota_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(compute_quota_model)
    user_group = UserGroupReadExtendedPublic.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0] == quota


def test_network_quota_read_ext(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    network_quota_model: NetworkQuota,
    network_service_model: NetworkService,
):
    with pytest.raises(CardinalityViolation):
        NetworkQuotaReadExtended.from_orm(network_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    network_quota_model.service.connect(network_service_model)
    quota = NetworkQuotaReadExtended.from_orm(network_quota_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(network_quota_model)
    user_group = UserGroupReadExtended.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0] == quota


def test_network_quota_read_ext_public(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    network_quota_model: NetworkQuota,
    network_service_model: NetworkService,
):
    with pytest.raises(CardinalityViolation):
        NetworkQuotaReadExtendedPublic.from_orm(network_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    network_quota_model.service.connect(network_service_model)
    quota = NetworkQuotaReadExtendedPublic.from_orm(network_quota_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(network_quota_model)
    user_group = UserGroupReadExtendedPublic.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0] == quota


def test_object_store_quota_read_ext(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    object_store_quota_model: ObjectStoreQuota,
    object_store_service_model: ObjectStoreService,
):
    with pytest.raises(CardinalityViolation):
        ObjectStoreQuotaReadExtended.from_orm(object_store_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(object_store_service_model)
    object_store_quota_model.service.connect(object_store_service_model)
    quota = ObjectStoreQuotaReadExtended.from_orm(object_store_quota_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(object_store_quota_model)
    user_group = UserGroupReadExtended.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0] == quota


def test_object_store_quota_read_ext_public(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    object_store_quota_model: ObjectStoreQuota,
    object_store_service_model: ObjectStoreService,
):
    with pytest.raises(CardinalityViolation):
        ObjectStoreQuotaReadExtendedPublic.from_orm(object_store_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(object_store_service_model)
    object_store_quota_model.service.connect(object_store_service_model)
    quota = ObjectStoreQuotaReadExtendedPublic.from_orm(object_store_quota_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(object_store_quota_model)
    user_group = UserGroupReadExtendedPublic.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0] == quota


def test_block_storage_service_read_ext(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    block_storage_quota_model: BlockStorageQuota,
    block_storage_service_model: BlockStorageService,
):
    with pytest.raises(CardinalityViolation):
        BlockStorageServiceReadExtended.from_orm(block_storage_service_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(block_storage_service_model)
    service = BlockStorageServiceReadExtended.from_orm(block_storage_service_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(block_storage_quota_model)
    block_storage_quota_model.service.connect(block_storage_service_model)
    user_group = UserGroupReadExtended.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0].service == service
    assert user_group.slas[0].projects[0].quotas[
        0
    ].service.region == RegionReadPublic.from_orm(region_model)


def test_block_storage_service_read_ext_public(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
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
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(block_storage_quota_model)
    block_storage_quota_model.service.connect(block_storage_service_model)
    user_group = UserGroupReadExtendedPublic.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0].service == service
    assert user_group.slas[0].projects[0].quotas[
        0
    ].service.region == RegionReadPublic.from_orm(region_model)


def test_compute_service_read_ext(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    compute_quota_model: ComputeQuota,
    compute_service_model: ComputeService,
):
    with pytest.raises(CardinalityViolation):
        ComputeServiceReadExtended.from_orm(compute_service_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    service = ComputeServiceReadExtended.from_orm(compute_service_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(compute_quota_model)
    compute_quota_model.service.connect(compute_service_model)
    user_group = UserGroupReadExtended.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0].service == service
    assert user_group.slas[0].projects[0].quotas[
        0
    ].service.region == RegionReadPublic.from_orm(region_model)


def test_compute_service_read_ext_public(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    compute_quota_model: ComputeQuota,
    compute_service_model: ComputeService,
):
    with pytest.raises(CardinalityViolation):
        ComputeServiceReadExtendedPublic.from_orm(compute_service_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    service = ComputeServiceReadExtendedPublic.from_orm(compute_service_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(compute_quota_model)
    compute_quota_model.service.connect(compute_service_model)
    user_group = UserGroupReadExtendedPublic.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0].service == service
    assert user_group.slas[0].projects[0].quotas[
        0
    ].service.region == RegionReadPublic.from_orm(region_model)


def test_network_service_read_ext(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    network_quota_model: NetworkQuota,
    network_service_model: NetworkService,
):
    with pytest.raises(CardinalityViolation):
        NetworkServiceReadExtended.from_orm(network_service_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    service = NetworkServiceReadExtended.from_orm(network_service_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(network_quota_model)
    network_quota_model.service.connect(network_service_model)
    user_group = UserGroupReadExtended.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0].service == service
    assert user_group.slas[0].projects[0].quotas[
        0
    ].service.region == RegionReadPublic.from_orm(region_model)


def test_network_service_read_ext_public(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    network_quota_model: NetworkQuota,
    network_service_model: NetworkService,
):
    with pytest.raises(CardinalityViolation):
        NetworkServiceReadExtendedPublic.from_orm(network_service_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    service = NetworkServiceReadExtendedPublic.from_orm(network_service_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(network_quota_model)
    network_quota_model.service.connect(network_service_model)
    user_group = UserGroupReadExtendedPublic.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0].service == service
    assert user_group.slas[0].projects[0].quotas[
        0
    ].service.region == RegionReadPublic.from_orm(region_model)


def test_object_store_service_read_ext(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    object_store_quota_model: ObjectStoreQuota,
    object_store_service_model: ObjectStoreService,
):
    with pytest.raises(CardinalityViolation):
        ObjectStoreServiceReadExtended.from_orm(object_store_service_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(object_store_service_model)
    service = ObjectStoreServiceReadExtended.from_orm(object_store_service_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(object_store_quota_model)
    object_store_quota_model.service.connect(object_store_service_model)
    user_group = UserGroupReadExtended.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0].service == service
    assert user_group.slas[0].projects[0].quotas[
        0
    ].service.region == RegionReadPublic.from_orm(region_model)


def test_object_store_service_read_ext_public(
    identity_provider_model: IdentityProvider,
    user_group_model: UserGroup,
    sla_model: SLA,
    project_model: Project,
    provider_model: Provider,
    region_model: Region,
    object_store_quota_model: ObjectStoreQuota,
    object_store_service_model: ObjectStoreService,
):
    with pytest.raises(CardinalityViolation):
        ObjectStoreServiceReadExtendedPublic.from_orm(object_store_service_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(object_store_service_model)
    service = ObjectStoreServiceReadExtendedPublic.from_orm(object_store_service_model)
    identity_provider_model.user_groups.connect(user_group_model)
    user_group_model.slas.connect(sla_model)
    sla_model.projects.connect(project_model)
    project_model.provider.connect(provider_model)
    project_model.quotas.connect(object_store_quota_model)
    object_store_quota_model.service.connect(object_store_service_model)
    user_group = UserGroupReadExtendedPublic.from_orm(user_group_model)
    assert len(user_group.slas) == 1
    assert len(user_group.slas[0].projects) == 1
    assert len(user_group.slas[0].projects[0].quotas) == 1
    assert user_group.slas[0].projects[0].quotas[0].service == service
    assert user_group.slas[0].projects[0].quotas[
        0
    ].service.region == RegionReadPublic.from_orm(region_model)
