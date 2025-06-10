import pytest
from neomodel.exceptions import CardinalityViolation

from fedreg.v1.core import BaseReadPrivateExtended, BaseReadPublicExtended
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
from fedreg.v1.quota.schemas_extended import (
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
    RegionReadExtended,
    RegionReadExtendedPublic,
)
from fedreg.v1.region.models import Region
from fedreg.v1.region.schemas import RegionRead, RegionReadPublic
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


def test_class_inheritance():
    assert issubclass(BlockStorageQuotaReadExtended, BaseReadPrivateExtended)
    assert issubclass(BlockStorageQuotaReadExtended, BlockStorageQuotaRead)
    assert (
        BlockStorageQuotaReadExtended.__fields__["schema_type"].default
        == "private_extended"
    )
    assert BlockStorageQuotaReadExtended.__config__.orm_mode is True

    assert issubclass(BlockStorageQuotaReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(BlockStorageQuotaReadExtendedPublic, BlockStorageQuotaReadPublic)
    assert (
        BlockStorageQuotaReadExtendedPublic.__fields__["schema_type"].default
        == "public_extended"
    )
    assert BlockStorageQuotaReadExtendedPublic.__config__.orm_mode is True

    assert issubclass(ComputeQuotaReadExtended, BaseReadPrivateExtended)
    assert issubclass(ComputeQuotaReadExtended, ComputeQuotaRead)
    assert (
        ComputeQuotaReadExtended.__fields__["schema_type"].default == "private_extended"
    )
    assert ComputeQuotaReadExtended.__config__.orm_mode is True

    assert issubclass(ComputeQuotaReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(ComputeQuotaReadExtendedPublic, ComputeQuotaReadPublic)
    assert (
        ComputeQuotaReadExtendedPublic.__fields__["schema_type"].default
        == "public_extended"
    )
    assert ComputeQuotaReadExtendedPublic.__config__.orm_mode is True

    assert issubclass(NetworkQuotaReadExtended, BaseReadPrivateExtended)
    assert issubclass(NetworkQuotaReadExtended, NetworkQuotaRead)
    assert (
        NetworkQuotaReadExtended.__fields__["schema_type"].default == "private_extended"
    )
    assert NetworkQuotaReadExtended.__config__.orm_mode is True

    assert issubclass(NetworkQuotaReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(NetworkQuotaReadExtendedPublic, NetworkQuotaReadPublic)
    assert (
        NetworkQuotaReadExtendedPublic.__fields__["schema_type"].default
        == "public_extended"
    )
    assert NetworkQuotaReadExtendedPublic.__config__.orm_mode is True

    assert issubclass(ObjectStoreQuotaReadExtended, BaseReadPrivateExtended)
    assert issubclass(ObjectStoreQuotaReadExtended, ObjectStoreQuotaRead)
    assert (
        ObjectStoreQuotaReadExtended.__fields__["schema_type"].default
        == "private_extended"
    )
    assert ObjectStoreQuotaReadExtended.__config__.orm_mode is True

    assert issubclass(ObjectStoreQuotaReadExtendedPublic, BaseReadPublicExtended)
    assert issubclass(ObjectStoreQuotaReadExtendedPublic, ObjectStoreQuotaReadPublic)
    assert (
        ObjectStoreQuotaReadExtendedPublic.__fields__["schema_type"].default
        == "public_extended"
    )
    assert ObjectStoreQuotaReadExtendedPublic.__config__.orm_mode is True

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

    assert issubclass(RegionReadExtended, RegionRead)
    assert issubclass(RegionReadExtendedPublic, RegionReadPublic)


def test_block_storage_read_ext(
    block_storage_quota_model: BlockStorageQuota,
    block_storage_service_model: BlockStorageService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(block_storage_service_model)
    block_storage_quota_model.service.connect(block_storage_service_model)
    block_storage_quota_model.project.connect(project_model)

    item = BlockStorageQuotaReadExtendedPublic.from_orm(block_storage_quota_model)
    assert item.service is not None
    assert item.service == BlockStorageServiceReadExtendedPublic.from_orm(
        block_storage_service_model
    )
    assert item.project is not None
    assert item.project == ProjectReadPublic.from_orm(project_model)

    item = BlockStorageQuotaReadExtended.from_orm(block_storage_quota_model)
    assert item.service is not None
    assert item.service == BlockStorageServiceReadExtended.from_orm(
        block_storage_service_model
    )
    assert item.project is not None
    assert item.project == ProjectRead.from_orm(project_model)


def test_compute_read_ext(
    compute_quota_model: ComputeQuota,
    compute_service_model: ComputeService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    compute_quota_model.service.connect(compute_service_model)
    compute_quota_model.project.connect(project_model)

    item = ComputeQuotaReadExtendedPublic.from_orm(compute_quota_model)
    assert item.service is not None
    assert item.service == ComputeServiceReadExtendedPublic.from_orm(
        compute_service_model
    )
    assert item.project is not None
    assert item.project == ProjectReadPublic.from_orm(project_model)

    item = ComputeQuotaReadExtended.from_orm(compute_quota_model)
    assert item.service is not None
    assert item.service == ComputeServiceReadExtended.from_orm(compute_service_model)
    assert item.project is not None
    assert item.project == ProjectRead.from_orm(project_model)


def test_network_read_ext(
    network_quota_model: NetworkQuota,
    network_service_model: NetworkService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    network_quota_model.service.connect(network_service_model)
    network_quota_model.project.connect(project_model)

    item = NetworkQuotaReadExtendedPublic.from_orm(network_quota_model)
    assert item.service is not None
    assert item.service == NetworkServiceReadExtendedPublic.from_orm(
        network_service_model
    )
    assert item.project is not None
    assert item.project == ProjectReadPublic.from_orm(project_model)

    item = NetworkQuotaReadExtended.from_orm(network_quota_model)
    assert item.service is not None
    assert item.service == NetworkServiceReadExtended.from_orm(network_service_model)
    assert item.project is not None
    assert item.project == ProjectRead.from_orm(project_model)


def test_object_store_read_ext(
    object_store_quota_model: ObjectStoreQuota,
    object_store_service_model: ObjectStoreService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(object_store_service_model)
    object_store_quota_model.service.connect(object_store_service_model)
    object_store_quota_model.project.connect(project_model)

    item = ObjectStoreQuotaReadExtendedPublic.from_orm(object_store_quota_model)
    assert item.service is not None
    assert item.service == ObjectStoreServiceReadExtendedPublic.from_orm(
        object_store_service_model
    )
    assert item.project is not None
    assert item.project == ProjectReadPublic.from_orm(project_model)

    item = ObjectStoreQuotaReadExtended.from_orm(object_store_quota_model)
    assert item.service is not None
    assert item.service == ObjectStoreServiceReadExtended.from_orm(
        object_store_service_model
    )
    assert item.project is not None
    assert item.project == ProjectRead.from_orm(project_model)


def test_block_storage_read_ext_missing_project(
    block_storage_quota_model: BlockStorageQuota,
    block_storage_service_model: BlockStorageService,
    region_model: Region,
    provider_model: Provider,
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(block_storage_service_model)
    block_storage_quota_model.service.connect(block_storage_service_model)
    with pytest.raises(CardinalityViolation):
        BlockStorageQuotaReadExtendedPublic.from_orm(block_storage_quota_model)


def test_block_storage_read_ext_missing_service(
    block_storage_quota_model: BlockStorageQuota, project_model: Project
) -> None:
    block_storage_quota_model.project.connect(project_model)
    with pytest.raises(CardinalityViolation):
        BlockStorageQuotaReadExtendedPublic.from_orm(block_storage_quota_model)


def test_compute_read_ext_missing_project(
    compute_quota_model: BlockStorageQuota,
    compute_service_model: BlockStorageService,
    region_model: Region,
    provider_model: Provider,
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    compute_quota_model.service.connect(compute_service_model)
    with pytest.raises(CardinalityViolation):
        BlockStorageQuotaReadExtendedPublic.from_orm(compute_quota_model)


def test_compute_read_ext_missing_service(
    compute_quota_model: BlockStorageQuota, project_model: Project
) -> None:
    compute_quota_model.project.connect(project_model)
    with pytest.raises(CardinalityViolation):
        BlockStorageQuotaReadExtendedPublic.from_orm(compute_quota_model)


def test_network_read_ext_missing_project(
    network_quota_model: BlockStorageQuota,
    network_service_model: BlockStorageService,
    region_model: Region,
    provider_model: Provider,
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    network_quota_model.service.connect(network_service_model)
    with pytest.raises(CardinalityViolation):
        BlockStorageQuotaReadExtendedPublic.from_orm(network_quota_model)


def test_network_read_ext_missing_service(
    network_quota_model: BlockStorageQuota, project_model: Project
) -> None:
    network_quota_model.project.connect(project_model)
    with pytest.raises(CardinalityViolation):
        BlockStorageQuotaReadExtendedPublic.from_orm(network_quota_model)


def test_object_store_read_ext_missing_project(
    object_store_quota_model: BlockStorageQuota,
    object_store_service_model: BlockStorageService,
    region_model: Region,
    provider_model: Provider,
) -> None:
    provider_model.regions.connect(region_model)
    region_model.services.connect(object_store_service_model)
    object_store_quota_model.service.connect(object_store_service_model)
    with pytest.raises(CardinalityViolation):
        BlockStorageQuotaReadExtendedPublic.from_orm(object_store_quota_model)


def test_object_store_read_ext_missing_service(
    object_store_quota_model: BlockStorageQuota, project_model: Project
) -> None:
    object_store_quota_model.project.connect(project_model)
    with pytest.raises(CardinalityViolation):
        BlockStorageQuotaReadExtendedPublic.from_orm(object_store_quota_model)


def test_block_storage_srv(
    block_storage_quota_model: BlockStorageQuota,
    block_storage_service_model: BlockStorageService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        BlockStorageServiceReadExtended.from_orm(block_storage_service_model)

    provider_model.regions.connect(region_model)
    region_model.services.connect(block_storage_service_model)
    service = BlockStorageServiceReadExtended.from_orm(block_storage_service_model)
    block_storage_quota_model.service.connect(block_storage_service_model)
    block_storage_quota_model.project.connect(project_model)
    quota = BlockStorageQuotaReadExtended.from_orm(block_storage_quota_model)
    assert quota.service == service
    assert service.region == RegionReadExtended.from_orm(region_model)


def test_block_storage_srv_public(
    block_storage_quota_model: BlockStorageQuota,
    block_storage_service_model: BlockStorageService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        BlockStorageServiceReadExtendedPublic.from_orm(block_storage_service_model)

    provider_model.regions.connect(region_model)
    region_model.services.connect(block_storage_service_model)
    service = BlockStorageServiceReadExtendedPublic.from_orm(
        block_storage_service_model
    )
    block_storage_quota_model.service.connect(block_storage_service_model)
    block_storage_quota_model.project.connect(project_model)
    quota = BlockStorageQuotaReadExtendedPublic.from_orm(block_storage_quota_model)
    assert quota.service == service
    assert service.region == RegionReadExtendedPublic.from_orm(region_model)


def test_compute_srv(
    compute_quota_model: ComputeQuota,
    compute_service_model: ComputeService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        ComputeServiceReadExtended.from_orm(compute_service_model)

    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    service = ComputeServiceReadExtended.from_orm(compute_service_model)
    compute_quota_model.service.connect(compute_service_model)
    compute_quota_model.project.connect(project_model)
    quota = ComputeQuotaReadExtended.from_orm(compute_quota_model)
    assert quota.service == service
    assert service.region == RegionReadExtended.from_orm(region_model)


def test_compute_srv_public(
    compute_quota_model: ComputeQuota,
    compute_service_model: ComputeService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        ComputeServiceReadExtendedPublic.from_orm(compute_service_model)

    provider_model.regions.connect(region_model)
    region_model.services.connect(compute_service_model)
    service = ComputeServiceReadExtendedPublic.from_orm(compute_service_model)
    compute_quota_model.service.connect(compute_service_model)
    compute_quota_model.project.connect(project_model)
    quota = ComputeQuotaReadExtendedPublic.from_orm(compute_quota_model)
    assert quota.service == service
    assert service.region == RegionReadExtendedPublic.from_orm(region_model)


def test_network_srv(
    network_quota_model: NetworkQuota,
    network_service_model: NetworkService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        NetworkServiceReadExtended.from_orm(network_service_model)

    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    service = NetworkServiceReadExtended.from_orm(network_service_model)
    network_quota_model.service.connect(network_service_model)
    network_quota_model.project.connect(project_model)
    quota = NetworkQuotaReadExtended.from_orm(network_quota_model)
    assert quota.service == service
    assert service.region == RegionReadExtended.from_orm(region_model)


def test_network_srv_public(
    network_quota_model: NetworkQuota,
    network_service_model: NetworkService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        NetworkServiceReadExtendedPublic.from_orm(network_service_model)

    provider_model.regions.connect(region_model)
    region_model.services.connect(network_service_model)
    service = NetworkServiceReadExtendedPublic.from_orm(network_service_model)
    network_quota_model.service.connect(network_service_model)
    network_quota_model.project.connect(project_model)
    quota = NetworkQuotaReadExtendedPublic.from_orm(network_quota_model)
    assert quota.service == service
    assert service.region == RegionReadExtendedPublic.from_orm(region_model)


def test_object_store_srv(
    object_store_quota_model: ObjectStoreQuota,
    object_store_service_model: ObjectStoreService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        ObjectStoreServiceReadExtended.from_orm(object_store_service_model)

    provider_model.regions.connect(region_model)
    region_model.services.connect(object_store_service_model)
    service = ObjectStoreServiceReadExtended.from_orm(object_store_service_model)
    object_store_quota_model.service.connect(object_store_service_model)
    object_store_quota_model.project.connect(project_model)
    quota = ObjectStoreQuotaReadExtended.from_orm(object_store_quota_model)
    assert quota.service == service
    assert service.region == RegionReadExtended.from_orm(region_model)


def test_object_store_srv_public(
    object_store_quota_model: ObjectStoreQuota,
    object_store_service_model: ObjectStoreService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        ObjectStoreServiceReadExtendedPublic.from_orm(object_store_service_model)

    provider_model.regions.connect(region_model)
    region_model.services.connect(object_store_service_model)
    service = ObjectStoreServiceReadExtendedPublic.from_orm(object_store_service_model)
    object_store_quota_model.service.connect(object_store_service_model)
    object_store_quota_model.project.connect(project_model)
    quota = ObjectStoreQuotaReadExtendedPublic.from_orm(object_store_quota_model)
    assert quota.service == service
    assert service.region == RegionReadExtendedPublic.from_orm(region_model)


def test_region(
    object_store_quota_model: ObjectStoreQuota,
    object_store_service_model: ObjectStoreService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        RegionReadExtended.from_orm(region_model)

    provider_model.regions.connect(region_model)
    region = RegionReadExtended.from_orm(region_model)
    region_model.services.connect(object_store_service_model)
    object_store_quota_model.service.connect(object_store_service_model)
    object_store_quota_model.project.connect(project_model)
    quota = ObjectStoreQuotaReadExtended.from_orm(object_store_quota_model)
    assert quota.service.region == region
    assert region.provider == ProviderRead.from_orm(provider_model)


def test_region_public(
    object_store_quota_model: ObjectStoreQuota,
    object_store_service_model: ObjectStoreService,
    region_model: Region,
    provider_model: Provider,
    project_model: Project,
) -> None:
    with pytest.raises(CardinalityViolation):
        RegionReadExtendedPublic.from_orm(region_model)

    provider_model.regions.connect(region_model)
    region = RegionReadExtendedPublic.from_orm(region_model)
    region_model.services.connect(object_store_service_model)
    object_store_quota_model.service.connect(object_store_service_model)
    object_store_quota_model.project.connect(project_model)
    quota = ObjectStoreQuotaReadExtendedPublic.from_orm(object_store_quota_model)
    assert quota.service.region == region
    assert region.provider == ProviderReadPublic.from_orm(provider_model)
