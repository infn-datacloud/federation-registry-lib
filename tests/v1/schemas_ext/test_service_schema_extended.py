import pytest
from neomodel.exceptions import CardinalityViolation
from pytest_cases import parametrize_with_cases

from fedreg.core import BaseReadPrivateExtended, BaseReadPublicExtended
from fedreg.project.models import Project
from fedreg.project.schemas import ProjectRead, ProjectReadPublic
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
    IdentityServiceRead,
    IdentityServiceReadPublic,
    NetworkServiceRead,
    NetworkServiceReadPublic,
    ObjectStoreServiceRead,
    ObjectStoreServiceReadPublic,
)
from fedreg.service.schemas_extended import (
    BlockStorageQuotaReadExtended,
    BlockStorageQuotaReadExtendedPublic,
    BlockStorageServiceReadExtended,
    BlockStorageServiceReadExtendedPublic,
    ComputeQuotaReadExtended,
    ComputeQuotaReadExtendedPublic,
    ComputeServiceReadExtended,
    ComputeServiceReadExtendedPublic,
    IdentityServiceReadExtended,
    IdentityServiceReadExtendedPublic,
    NetworkQuotaReadExtended,
    NetworkQuotaReadExtendedPublic,
    NetworkServiceReadExtended,
    NetworkServiceReadExtendedPublic,
    ObjectStoreQuotaReadExtended,
    ObjectStoreQuotaReadExtendedPublic,
    ObjectStoreServiceReadExtended,
    ObjectStoreServiceReadExtendedPublic,
    RegionReadExtended,
    RegionReadExtendedPublic,
)


def test_class_inheritance():
    assert issubclass(BlockStorageServiceReadExtended, BaseReadPrivateExtended)
    assert issubclass(BlockStorageServiceReadExtended, BlockStorageServiceRead)
    assert (
        BlockStorageServiceReadExtended.__fields__["schema_type"].default
        == "private_extended"
    )
    assert BlockStorageServiceReadExtended.__config__.orm_mode is True

    assert issubclass(BlockStorageServiceReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(
        BlockStorageServiceReadExtendedPublic, BlockStorageServiceReadPublic
    )
    assert (
        BlockStorageServiceReadExtendedPublic.__fields__["schema_type"].default
        == "public_extended"
    )
    assert BlockStorageServiceReadExtendedPublic.__config__.orm_mode is True

    assert issubclass(ComputeServiceReadExtended, BaseReadPrivateExtended)
    assert issubclass(ComputeServiceReadExtended, ComputeServiceRead)
    assert (
        ComputeServiceReadExtended.__fields__["schema_type"].default
        == "private_extended"
    )
    assert ComputeServiceReadExtended.__config__.orm_mode is True

    assert issubclass(ComputeServiceReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(ComputeServiceReadExtendedPublic, ComputeServiceReadPublic)
    assert (
        ComputeServiceReadExtendedPublic.__fields__["schema_type"].default
        == "public_extended"
    )
    assert ComputeServiceReadExtendedPublic.__config__.orm_mode is True

    assert issubclass(IdentityServiceReadExtended, BaseReadPrivateExtended)
    assert issubclass(IdentityServiceReadExtended, IdentityServiceRead)
    assert (
        IdentityServiceReadExtended.__fields__["schema_type"].default
        == "private_extended"
    )
    assert IdentityServiceReadExtended.__config__.orm_mode is True

    assert issubclass(IdentityServiceReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(IdentityServiceReadExtendedPublic, IdentityServiceReadPublic)
    assert (
        IdentityServiceReadExtendedPublic.__fields__["schema_type"].default
        == "public_extended"
    )
    assert IdentityServiceReadExtendedPublic.__config__.orm_mode is True

    assert issubclass(NetworkServiceReadExtended, BaseReadPrivateExtended)
    assert issubclass(NetworkServiceReadExtended, NetworkServiceRead)
    assert (
        NetworkServiceReadExtended.__fields__["schema_type"].default
        == "private_extended"
    )
    assert NetworkServiceReadExtended.__config__.orm_mode is True

    assert issubclass(NetworkServiceReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(NetworkServiceReadExtendedPublic, NetworkServiceReadPublic)
    assert (
        NetworkServiceReadExtendedPublic.__fields__["schema_type"].default
        == "public_extended"
    )
    assert NetworkServiceReadExtendedPublic.__config__.orm_mode is True

    assert issubclass(ObjectStoreServiceReadExtended, BaseReadPrivateExtended)
    assert issubclass(ObjectStoreServiceReadExtended, ObjectStoreServiceRead)
    assert (
        ObjectStoreServiceReadExtended.__fields__["schema_type"].default
        == "private_extended"
    )
    assert ObjectStoreServiceReadExtended.__config__.orm_mode is True

    assert issubclass(ObjectStoreServiceReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(
        ObjectStoreServiceReadExtendedPublic, ObjectStoreServiceReadPublic
    )
    assert (
        ObjectStoreServiceReadExtendedPublic.__fields__["schema_type"].default
        == "public_extended"
    )
    assert ObjectStoreServiceReadExtendedPublic.__config__.orm_mode is True

    assert issubclass(BlockStorageQuotaReadExtended, BlockStorageQuotaRead)
    assert issubclass(BlockStorageQuotaReadExtendedPublic, BlockStorageQuotaReadPublic)

    assert issubclass(ComputeQuotaReadExtended, ComputeQuotaRead)
    assert issubclass(ComputeQuotaReadExtendedPublic, ComputeQuotaReadPublic)

    assert issubclass(NetworkQuotaReadExtended, NetworkQuotaRead)
    assert issubclass(NetworkQuotaReadExtendedPublic, NetworkQuotaReadPublic)

    assert issubclass(ObjectStoreQuotaReadExtended, ObjectStoreQuotaRead)
    assert issubclass(ObjectStoreQuotaReadExtendedPublic, ObjectStoreQuotaReadPublic)

    assert issubclass(RegionReadExtended, RegionRead)
    assert issubclass(RegionReadExtendedPublic, RegionReadPublic)


@parametrize_with_cases("quotas", has_tag=("quotas", "block_storage"))
def test_block_storage_read_ext(
    block_storage_service_model: BlockStorageService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
    quotas: list[BlockStorageQuota],
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(block_storage_service_model)
    for quota in quotas:
        block_storage_service_model.quotas.connect(quota)
        project_model.quotas.connect(quota)

    item = BlockStorageServiceReadExtendedPublic.from_orm(block_storage_service_model)
    assert item.region == RegionReadExtendedPublic.from_orm(region_model)
    assert len(item.quotas) == len(quotas)

    item = BlockStorageServiceReadExtended.from_orm(block_storage_service_model)
    assert item.region == RegionReadExtended.from_orm(region_model)
    assert len(item.quotas) == len(quotas)


@parametrize_with_cases("quotas", has_tag=("quotas", "compute"))
def test_compute_read_ext(
    compute_service_model: ComputeService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
    quotas: list[ComputeQuota],
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    for quota in quotas:
        compute_service_model.quotas.connect(quota)
        project_model.quotas.connect(quota)

    item = ComputeServiceReadExtendedPublic.from_orm(compute_service_model)
    assert item.region == RegionReadExtendedPublic.from_orm(region_model)
    assert len(item.quotas) == len(quotas)

    item = ComputeServiceReadExtended.from_orm(compute_service_model)
    assert item.region == RegionReadExtended.from_orm(region_model)
    assert len(item.quotas) == len(quotas)


def test_identity_read_ext(
    identity_service_model: IdentityService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(identity_service_model)

    item = IdentityServiceReadExtendedPublic.from_orm(identity_service_model)
    assert item.region == RegionReadExtendedPublic.from_orm(region_model)

    item = IdentityServiceReadExtended.from_orm(identity_service_model)
    assert item.region == RegionReadExtended.from_orm(region_model)


@parametrize_with_cases("quotas", has_tag=("quotas", "network"))
def test_network_read_ext(
    network_service_model: NetworkService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
    quotas: list[NetworkQuota],
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    for quota in quotas:
        network_service_model.quotas.connect(quota)
        project_model.quotas.connect(quota)

    item = NetworkServiceReadExtendedPublic.from_orm(network_service_model)
    assert item.region == RegionReadExtendedPublic.from_orm(region_model)
    assert len(item.quotas) == len(quotas)

    item = NetworkServiceReadExtended.from_orm(network_service_model)
    assert item.region == RegionReadExtended.from_orm(region_model)
    assert len(item.quotas) == len(quotas)


@parametrize_with_cases("quotas", has_tag=("quotas", "object_store"))
def test_object_store_read_ext(
    object_store_service_model: ObjectStoreService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
    quotas: list[ObjectStoreQuota],
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(object_store_service_model)
    for quota in quotas:
        object_store_service_model.quotas.connect(quota)
        project_model.quotas.connect(quota)

    item = ObjectStoreServiceReadExtendedPublic.from_orm(object_store_service_model)
    assert item.region == RegionReadExtendedPublic.from_orm(region_model)
    assert len(item.quotas) == len(quotas)

    item = ObjectStoreServiceReadExtended.from_orm(object_store_service_model)
    assert item.region == RegionReadExtended.from_orm(region_model)
    assert len(item.quotas) == len(quotas)


def test_block_storage_quota_read_extended(
    block_storage_quota_model: BlockStorageQuota,
    block_storage_service_model: BlockStorageService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        BlockStorageQuotaReadExtended.from_orm(block_storage_quota_model)
    block_storage_quota_model.project.connect(project_model)
    quota = BlockStorageQuotaReadExtended.from_orm(block_storage_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(block_storage_service_model)
    block_storage_service_model.quotas.connect(block_storage_quota_model)
    service = BlockStorageServiceReadExtended.from_orm(block_storage_service_model)
    assert len(service.quotas) == 1
    assert service.quotas[0] == quota
    assert service.quotas[0].project == ProjectRead.from_orm(project_model)


def test_block_storage_quota_read_extended_public(
    block_storage_quota_model: BlockStorageQuota,
    block_storage_service_model: BlockStorageService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        BlockStorageQuotaReadExtendedPublic.from_orm(block_storage_quota_model)
    block_storage_quota_model.project.connect(project_model)
    quota = BlockStorageQuotaReadExtendedPublic.from_orm(block_storage_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(block_storage_service_model)
    block_storage_service_model.quotas.connect(block_storage_quota_model)
    service = BlockStorageServiceReadExtendedPublic.from_orm(
        block_storage_service_model
    )
    assert len(service.quotas) == 1
    assert service.quotas[0] == quota
    assert service.quotas[0].project == ProjectReadPublic.from_orm(project_model)


def test_compute_quota_read_extended(
    compute_quota_model: ComputeQuota,
    compute_service_model: ComputeService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        ComputeQuotaReadExtended.from_orm(compute_quota_model)
    compute_quota_model.project.connect(project_model)
    quota = ComputeQuotaReadExtended.from_orm(compute_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    compute_service_model.quotas.connect(compute_quota_model)
    service = ComputeServiceReadExtended.from_orm(compute_service_model)
    assert len(service.quotas) == 1
    assert service.quotas[0] == quota
    assert service.quotas[0].project == ProjectRead.from_orm(project_model)


def test_compute_quota_read_extended_public(
    compute_quota_model: ComputeQuota,
    compute_service_model: ComputeService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        ComputeQuotaReadExtendedPublic.from_orm(compute_quota_model)
    compute_quota_model.project.connect(project_model)
    quota = ComputeQuotaReadExtendedPublic.from_orm(compute_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    compute_service_model.quotas.connect(compute_quota_model)
    service = ComputeServiceReadExtendedPublic.from_orm(compute_service_model)
    assert len(service.quotas) == 1
    assert service.quotas[0] == quota
    assert service.quotas[0].project == ProjectReadPublic.from_orm(project_model)


def test_network_quota_read_extended(
    network_quota_model: NetworkQuota,
    network_service_model: NetworkService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        NetworkQuotaReadExtended.from_orm(network_quota_model)
    network_quota_model.project.connect(project_model)
    quota = NetworkQuotaReadExtended.from_orm(network_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    network_service_model.quotas.connect(network_quota_model)
    service = NetworkServiceReadExtended.from_orm(network_service_model)
    assert len(service.quotas) == 1
    assert service.quotas[0] == quota
    assert service.quotas[0].project == ProjectRead.from_orm(project_model)


def test_network_quota_read_extended_public(
    network_quota_model: NetworkQuota,
    network_service_model: NetworkService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        NetworkQuotaReadExtendedPublic.from_orm(network_quota_model)
    network_quota_model.project.connect(project_model)
    quota = NetworkQuotaReadExtendedPublic.from_orm(network_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    network_service_model.quotas.connect(network_quota_model)
    service = NetworkServiceReadExtendedPublic.from_orm(network_service_model)
    assert len(service.quotas) == 1
    assert service.quotas[0] == quota
    assert service.quotas[0].project == ProjectReadPublic.from_orm(project_model)


def test_object_store_quota_read_extended(
    object_store_quota_model: ObjectStoreQuota,
    object_store_service_model: ObjectStoreService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        ObjectStoreQuotaReadExtended.from_orm(object_store_quota_model)
    object_store_quota_model.project.connect(project_model)
    quota = ObjectStoreQuotaReadExtended.from_orm(object_store_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(object_store_service_model)
    object_store_service_model.quotas.connect(object_store_quota_model)
    service = ObjectStoreServiceReadExtended.from_orm(object_store_service_model)
    assert len(service.quotas) == 1
    assert service.quotas[0] == quota
    assert service.quotas[0].project == ProjectRead.from_orm(project_model)


def test_object_store_quota_read_extended_public(
    object_store_quota_model: ObjectStoreQuota,
    object_store_service_model: ObjectStoreService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        ObjectStoreQuotaReadExtendedPublic.from_orm(object_store_quota_model)
    object_store_quota_model.project.connect(project_model)
    quota = ObjectStoreQuotaReadExtendedPublic.from_orm(object_store_quota_model)
    provider_model.regions.connect(region_model)
    region_model.services.connect(object_store_service_model)
    object_store_service_model.quotas.connect(object_store_quota_model)
    service = ObjectStoreServiceReadExtendedPublic.from_orm(object_store_service_model)
    assert len(service.quotas) == 1
    assert service.quotas[0] == quota
    assert service.quotas[0].project == ProjectReadPublic.from_orm(project_model)


def test_region_read_extended(
    block_storage_service_model: BlockStorageService,
    region_model: Region,
    provider_model: Provider,
) -> None:
    with pytest.raises(CardinalityViolation):
        RegionReadExtended.from_orm(region_model)
    region_model.provider.connect(provider_model)
    region = RegionReadExtended.from_orm(region_model)
    block_storage_service_model.region.connect(region_model)
    service = BlockStorageServiceReadExtended.from_orm(block_storage_service_model)
    assert service.region == region
    assert service.region.provider == ProviderRead.from_orm(provider_model)


def test_region_read_extended_public(
    block_storage_service_model: BlockStorageService,
    region_model: Region,
    provider_model: Provider,
) -> None:
    with pytest.raises(CardinalityViolation):
        RegionReadExtendedPublic.from_orm(region_model)
    region_model.provider.connect(provider_model)
    region = RegionReadExtendedPublic.from_orm(region_model)
    block_storage_service_model.region.connect(region_model)
    service = BlockStorageServiceReadExtendedPublic.from_orm(
        block_storage_service_model
    )
    assert service.region == region
    assert service.region.provider == ProviderReadPublic.from_orm(provider_model)
