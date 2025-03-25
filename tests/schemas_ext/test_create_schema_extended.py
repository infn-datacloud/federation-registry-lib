import pytest
from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from fedreg.flavor.schemas import PrivateFlavorCreate, SharedFlavorCreate
from fedreg.identity_provider.schemas import IdentityProviderCreate
from fedreg.image.schemas import PrivateImageCreate, SharedImageCreate
from fedreg.location.schemas import LocationCreate
from fedreg.network.schemas import PrivateNetworkCreate, SharedNetworkCreate
from fedreg.project.schemas import ProjectCreate
from fedreg.provider.schemas import ProviderCreate
from fedreg.provider.schemas_extended import (
    BlockStorageQuotaCreateExtended,
    BlockStorageServiceCreateExtended,
    ComputeQuotaCreateExtended,
    ComputeServiceCreateExtended,
    IdentityProviderCreateExtended,
    NetworkQuotaCreateExtended,
    NetworkServiceCreateExtended,
    ObjectStoreQuotaCreateExtended,
    ObjectStoreServiceCreateExtended,
    PrivateFlavorCreateExtended,
    PrivateImageCreateExtended,
    PrivateNetworkCreateExtended,
    ProviderCreateExtended,
    RegionCreateExtended,
    SLACreateExtended,
    UserGroupCreateExtended,
)
from fedreg.quota.schemas import (
    BlockStorageQuotaCreate,
    ComputeQuotaCreate,
    NetworkQuotaCreate,
    ObjectStoreQuotaCreate,
)
from fedreg.region.schemas import RegionCreate
from fedreg.service.enum import ServiceType
from fedreg.service.schemas import (
    BlockStorageServiceCreate,
    ComputeServiceCreate,
    NetworkServiceCreate,
    ObjectStoreServiceCreate,
)
from fedreg.sla.schemas import SLACreate
from fedreg.user_group.schemas import UserGroupCreate
from tests.schemas.utils import (
    flavor_schema_dict,
    image_schema_dict,
    network_schema_dict,
    provider_schema_dict,
    quota_schema_dict,
    region_schema_dict,
    service_schema_dict,
)
from tests.utils import random_lower_string


def test_inheritance() -> None:
    assert issubclass(ProviderCreateExtended, ProviderCreate)

    assert issubclass(IdentityProviderCreateExtended, IdentityProviderCreate)
    assert issubclass(UserGroupCreateExtended, UserGroupCreate)
    assert issubclass(SLACreateExtended, SLACreate)

    assert issubclass(RegionCreateExtended, RegionCreate)
    assert issubclass(BlockStorageServiceCreateExtended, BlockStorageServiceCreate)
    assert issubclass(ComputeServiceCreateExtended, ComputeServiceCreate)
    assert issubclass(NetworkServiceCreateExtended, NetworkServiceCreate)
    assert issubclass(ObjectStoreServiceCreateExtended, ObjectStoreServiceCreate)
    assert issubclass(BlockStorageQuotaCreateExtended, BlockStorageQuotaCreate)
    assert issubclass(ComputeQuotaCreateExtended, ComputeQuotaCreate)
    assert issubclass(NetworkQuotaCreateExtended, NetworkQuotaCreate)
    assert issubclass(ObjectStoreQuotaCreateExtended, ObjectStoreQuotaCreate)

    assert issubclass(PrivateFlavorCreateExtended, PrivateFlavorCreate)
    assert issubclass(PrivateImageCreateExtended, PrivateImageCreate)
    assert issubclass(PrivateNetworkCreateExtended, PrivateNetworkCreate)


def test_provider_create_ext() -> None:
    provider = ProviderCreateExtended(**provider_schema_dict())
    assert len(provider.projects) == 0
    assert len(provider.regions) == 0
    assert len(provider.identity_providers) == 0


@parametrize_with_cases("projects", has_tag=("projects", "valid"))
def test_provider_create_ext_with_projects(projects: list[dict]) -> None:
    projects = [ProjectCreate(**project) for project in projects]
    provider = ProviderCreateExtended(**provider_schema_dict(), projects=projects)
    assert len(provider.projects) == len(projects)
    assert len(provider.regions) == 0
    assert len(provider.identity_providers) == 0


@parametrize_with_cases("projects", has_tag=("projects", "duplicate"))
def test_provider_create_ext_with_dup_projects(projects: list[dict]) -> None:
    projects = [ProjectCreate(**project) for project in projects]
    with pytest.raises(
        ValidationError, match="There are multiple items with identical"
    ):
        ProviderCreateExtended(**provider_schema_dict(), projects=projects)


@parametrize_with_cases(
    "identity_providers, projects_uuid", has_tag=("identity_providers", "valid")
)
def test_provider_create_ext_with_identity_providers(
    identity_providers: list[dict], projects_uuid: list[dict]
) -> None:
    projects = [
        ProjectCreate(uuid=project, name=random_lower_string())
        for project in projects_uuid
    ]
    identity_providers = [
        IdentityProviderCreateExtended(**identity_provider)
        for identity_provider in identity_providers
    ]
    provider = ProviderCreateExtended(
        **provider_schema_dict(),
        identity_providers=identity_providers,
        projects=projects,
    )
    assert len(provider.projects) == len(projects)
    assert len(provider.regions) == 0
    assert len(provider.identity_providers) == len(identity_providers)


@parametrize_with_cases(
    "identity_providers, projects_uuid", has_tag=("identity_providers", "duplicate")
)
def test_provider_create_ext_with_dup_idp(
    identity_providers: list[dict], projects_uuid: list[str]
) -> None:
    projects = [
        ProjectCreate(uuid=project, name=random_lower_string())
        for project in projects_uuid
    ]
    identity_providers = [
        IdentityProviderCreateExtended(**idp) for idp in identity_providers
    ]
    with pytest.raises(
        ValidationError, match="There are multiple items with identical endpoint"
    ):
        ProviderCreateExtended(
            **provider_schema_dict(),
            identity_providers=identity_providers,
            projects=projects,
        )


@parametrize_with_cases(
    "identity_provider, projects_uuid", has_tag=("identity_providers", "slas")
)
def test_provider_create_ext_dup_slas(
    identity_provider: dict, projects_uuid: list[str]
) -> None:
    projects = [
        ProjectCreate(uuid=project, name=random_lower_string())
        for project in projects_uuid
    ]
    identity_providers = [IdentityProviderCreateExtended(**identity_provider)]
    with pytest.raises(ValidationError, match="already used by another user group"):
        ProviderCreateExtended(
            **provider_schema_dict(),
            identity_providers=identity_providers,
            projects=projects,
        )


@parametrize_with_cases(
    "identity_provider, projects_uuid", has_tag=("identity_providers", "projects")
)
def test_provider_create_ext_dup_projects(
    identity_provider: dict, projects_uuid: list[str]
) -> None:
    projects = [
        ProjectCreate(uuid=project, name=random_lower_string())
        for project in projects_uuid
    ]
    identity_providers = [IdentityProviderCreateExtended(**identity_provider)]
    with pytest.raises(ValidationError, match="already used by another SLA"):
        ProviderCreateExtended(
            **provider_schema_dict(),
            identity_providers=identity_providers,
            projects=projects,
        )


@parametrize_with_cases(
    "identity_provider", has_tag=("identity_providers", "no-project")
)
def test_provider_create_ext_idp_project_mismatch(identity_provider: dict) -> None:
    identity_providers = [IdentityProviderCreateExtended(**identity_provider)]
    with pytest.raises(ValidationError, match="not in this provider"):
        ProviderCreateExtended(
            **provider_schema_dict(), identity_providers=identity_providers
        )


@parametrize_with_cases("identity_provider", has_tag=("identity_provider", "valid"))
def test_identity_provider_create_ext(identity_provider: dict) -> None:
    idp = IdentityProviderCreateExtended(**identity_provider)
    assert len(idp.user_groups) == len(identity_provider.get("user_groups", []))
    if len(idp.user_groups) == 1:
        assert isinstance(idp.user_groups[0], UserGroupCreateExtended)


@parametrize_with_cases("identity_provider", has_tag=("identity_provider", "invalid"))
def test_identity_provider_create_ext_invalid(identity_provider: dict) -> None:
    with pytest.raises(
        ValidationError, match="1 validation error for IdentityProviderCreateExtended"
    ):
        IdentityProviderCreateExtended(**identity_provider)


@parametrize_with_cases("user_group", has_tag=("user_group", "valid"))
def test_user_group_create_ext(user_group: dict) -> None:
    item = UserGroupCreateExtended(**user_group)
    sla = user_group.get("sla", None)
    if sla is not None:
        assert item.sla is not None
        assert isinstance(item.sla, SLACreateExtended)
    else:
        assert item.sla is None


@parametrize_with_cases("user_group", has_tag=("user_group", "invalid"))
def test_user_group_create_ext_invalid(user_group: dict) -> None:
    with pytest.raises(
        ValidationError, match="1 validation error for UserGroupCreateExtended"
    ):
        UserGroupCreateExtended(**user_group)


@parametrize_with_cases("sla", has_tag=("sla", "valid"))
def test_sla_create_ext(sla: dict) -> None:
    item = SLACreateExtended(**sla)
    assert item.project is not None
    assert isinstance(item.project, str)


@parametrize_with_cases("sla", has_tag=("sla", "invalid"))
def test_sla_create_ext_invalid(sla: dict) -> None:
    with pytest.raises(
        ValidationError, match="1 validation error for SLACreateExtended"
    ):
        SLACreateExtended(**sla)


@parametrize_with_cases("regions", has_tag=("regions", "valid", "base"))
def test_provider_create_ext_with_regions(regions: list[dict]) -> None:
    regions = [RegionCreateExtended(**region) for region in regions]
    provider = ProviderCreateExtended(**provider_schema_dict(), regions=regions)
    assert len(provider.projects) == 0
    assert len(provider.regions) == len(regions)
    assert len(provider.identity_providers) == 0


@parametrize_with_cases("region, project_uuid", has_tag=("regions", "valid", "project"))
def test_provider_create_ext_with_regions_and_projects(
    region: dict, project_uuid: str
) -> None:
    projects = [ProjectCreate(uuid=project_uuid, name=random_lower_string())]
    regions = [RegionCreateExtended(**region)]
    provider = ProviderCreateExtended(
        **provider_schema_dict(), regions=regions, projects=projects
    )
    assert len(provider.projects) == len(projects)
    assert len(provider.regions) == len(regions)
    assert len(provider.identity_providers) == 0


@parametrize_with_cases("regions", has_tag=("regions", "duplicate"))
def test_provider_create_ext_with_dup_reg(regions: list[dict]) -> None:
    regions = [RegionCreateExtended(**idp) for idp in regions]
    with pytest.raises(
        ValidationError, match="There are multiple items with identical name"
    ):
        ProviderCreateExtended(**provider_schema_dict(), regions=regions)


@parametrize_with_cases("region", has_tag=("regions", "no-project"))
def test_provider_create_ext_region_project_mismatch(region: dict) -> None:
    regions = [RegionCreateExtended(**region)]
    with pytest.raises(ValidationError, match="not in this provider"):
        ProviderCreateExtended(**provider_schema_dict(), regions=regions)


@parametrize_with_cases("location", has_tag=("region", "location"))
def test_region_create_ext(location: dict | None) -> None:
    item = RegionCreateExtended(**region_schema_dict(), location=location)
    if location:
        assert isinstance(item.location, LocationCreate)
    else:
        assert item.location is None
    assert len(item.block_storage_services) == 0
    assert len(item.compute_services) == 0
    assert len(item.identity_services) == 0
    assert len(item.network_services) == 0
    assert len(item.object_store_services) == 0


@parametrize_with_cases(
    "services", has_tag=("region", "services", "block-storage", "valid")
)
def test_region_create_ext_with_block_storage_srv(services: list[dict]) -> None:
    item = RegionCreateExtended(**region_schema_dict(), block_storage_services=services)
    assert item.location is None
    assert len(item.block_storage_services) == len(services)
    assert len(item.compute_services) == 0
    assert len(item.identity_services) == 0
    assert len(item.network_services) == 0
    assert len(item.object_store_services) == 0


@parametrize_with_cases("services", has_tag=("region", "services", "compute", "valid"))
def test_region_create_ext_with_compute_srv(services: list[dict]) -> None:
    item = RegionCreateExtended(**region_schema_dict(), compute_services=services)
    assert item.location is None
    assert len(item.block_storage_services) == 0
    assert len(item.compute_services) == len(services)
    assert len(item.identity_services) == 0
    assert len(item.network_services) == 0
    assert len(item.object_store_services) == 0


@parametrize_with_cases("services", has_tag=("region", "services", "identity", "valid"))
def test_region_create_ext_with_identity_srv(services: list[dict]) -> None:
    item = RegionCreateExtended(**region_schema_dict(), identity_services=services)
    assert item.location is None
    assert len(item.block_storage_services) == 0
    assert len(item.compute_services) == 0
    assert len(item.identity_services) == len(services)
    assert len(item.network_services) == 0
    assert len(item.object_store_services) == 0


@parametrize_with_cases("services", has_tag=("region", "services", "network", "valid"))
def test_region_create_ext_with_network_srv(services: list[dict]) -> None:
    item = RegionCreateExtended(**region_schema_dict(), network_services=services)
    assert item.location is None
    assert len(item.block_storage_services) == 0
    assert len(item.compute_services) == 0
    assert len(item.identity_services) == 0
    assert len(item.network_services) == len(services)
    assert len(item.object_store_services) == 0


@parametrize_with_cases(
    "services", has_tag=("region", "services", "object-store", "valid")
)
def test_region_create_ext_with_object_store_srv(services: list[dict]) -> None:
    item = RegionCreateExtended(**region_schema_dict(), object_store_services=services)
    assert item.location is None
    assert len(item.block_storage_services) == 0
    assert len(item.compute_services) == 0
    assert len(item.identity_services) == 0
    assert len(item.network_services) == 0
    assert len(item.object_store_services) == len(services)


@parametrize_with_cases(
    "services", has_tag=("region", "services", "block-storage", "invalid")
)
def test_region_create_ext_dup_block_storage_srv(services: list[dict]) -> None:
    with pytest.raises(
        ValidationError, match="There are multiple items with identical endpoint"
    ):
        RegionCreateExtended(**region_schema_dict(), block_storage_services=services)


@parametrize_with_cases(
    "services", has_tag=("region", "services", "compute", "invalid")
)
def test_region_create_ext_dup_compute_srv(services: list[dict]) -> None:
    with pytest.raises(
        ValidationError, match="There are multiple items with identical endpoint"
    ):
        RegionCreateExtended(**region_schema_dict(), compute_services=services)


@parametrize_with_cases(
    "services", has_tag=("region", "services", "identity", "invalid")
)
def test_region_create_ext_dup_identity_srv(services: list[dict]) -> None:
    with pytest.raises(
        ValidationError, match="There are multiple items with identical endpoint"
    ):
        RegionCreateExtended(**region_schema_dict(), identity_services=services)


@parametrize_with_cases(
    "services", has_tag=("region", "services", "network", "invalid")
)
def test_region_create_ext_dup_network_srv(services: list[dict]) -> None:
    with pytest.raises(
        ValidationError, match="There are multiple items with identical endpoint"
    ):
        RegionCreateExtended(**region_schema_dict(), network_services=services)


@parametrize_with_cases(
    "services", has_tag=("region", "services", "object-store", "invalid")
)
def test_region_create_ext_dup_object_store_srv(services: list[dict]) -> None:
    with pytest.raises(
        ValidationError, match="There are multiple items with identical endpoint"
    ):
        RegionCreateExtended(**region_schema_dict(), object_store_services=services)


def test_block_storage_srv_create_ext() -> None:
    srv = BlockStorageServiceCreateExtended(
        **service_schema_dict(srv_type=ServiceType.BLOCK_STORAGE)
    )
    assert len(srv.quotas) == 0


@parametrize_with_cases("quotas", has_tag=("service", "block-storage", "quotas"))
def test_block_storage_srv_create_ext_with_quotas(quotas: list[dict]) -> None:
    srv = BlockStorageServiceCreateExtended(
        **service_schema_dict(srv_type=ServiceType.BLOCK_STORAGE), quotas=quotas
    )
    assert len(srv.quotas) == len(quotas)
    assert isinstance(srv.quotas[0], BlockStorageQuotaCreateExtended)


def test_compute_srv_create_ext() -> None:
    srv = ComputeServiceCreateExtended(
        **service_schema_dict(srv_type=ServiceType.COMPUTE)
    )
    assert len(srv.quotas) == 0
    assert len(srv.flavors) == 0
    assert len(srv.images) == 0


@parametrize_with_cases("quotas", has_tag=("service", "compute", "quotas"))
def test_compute_srv_create_ext_with_quotas(quotas: list[dict]) -> None:
    srv = ComputeServiceCreateExtended(
        **service_schema_dict(srv_type=ServiceType.COMPUTE), quotas=quotas
    )
    assert len(srv.quotas) == len(quotas)
    assert isinstance(srv.quotas[0], ComputeQuotaCreateExtended)
    assert len(srv.flavors) == 0
    assert len(srv.images) == 0


@parametrize_with_cases("flavors", has_tag=("service", "compute", "flavors"))
def test_compute_srv_create_ext_with_flavors(flavors: list[dict]) -> None:
    srv = ComputeServiceCreateExtended(
        **service_schema_dict(srv_type=ServiceType.COMPUTE), flavors=flavors
    )
    assert len(srv.quotas) == 0
    assert len(srv.flavors) == len(flavors)
    if "projects" in flavors[0].keys():
        assert isinstance(srv.flavors[0], PrivateFlavorCreateExtended)
    else:
        assert isinstance(srv.flavors[0], SharedFlavorCreate)
    assert len(srv.images) == 0


@parametrize_with_cases("images", has_tag=("service", "compute", "images"))
def test_compute_srv_create_ext_with_images(images: list[dict]) -> None:
    srv = ComputeServiceCreateExtended(
        **service_schema_dict(srv_type=ServiceType.COMPUTE), images=images
    )
    assert len(srv.quotas) == 0
    assert len(srv.flavors) == 0
    assert len(srv.images) == len(images)
    if "projects" in images[0].keys():
        assert isinstance(srv.images[0], PrivateImageCreateExtended)
    else:
        assert isinstance(srv.images[0], SharedImageCreate)


def test_network_srv_create_ext() -> None:
    srv = NetworkServiceCreateExtended(
        **service_schema_dict(srv_type=ServiceType.NETWORK)
    )
    assert len(srv.quotas) == 0
    assert len(srv.networks) == 0


@parametrize_with_cases("quotas", has_tag=("service", "network", "quotas"))
def test_network_srv_create_ext_with_quotas(quotas: list[dict]) -> None:
    srv = NetworkServiceCreateExtended(
        **service_schema_dict(srv_type=ServiceType.NETWORK), quotas=quotas
    )
    assert len(srv.quotas) == len(quotas)
    assert isinstance(srv.quotas[0], NetworkQuotaCreateExtended)
    assert len(srv.networks) == 0


@parametrize_with_cases("networks", has_tag=("service", "network", "networks"))
def test_network_srv_create_ext_with_networks(networks: list[dict]) -> None:
    srv = NetworkServiceCreateExtended(
        **service_schema_dict(srv_type=ServiceType.NETWORK), networks=networks
    )
    assert len(srv.quotas) == 0
    assert len(srv.networks) == len(networks)
    if "projects" in networks[0].keys():
        assert isinstance(srv.networks[0], PrivateNetworkCreateExtended)
    else:
        assert isinstance(srv.networks[0], SharedNetworkCreate)


def test_object_store_srv_create_ext() -> None:
    srv = ObjectStoreServiceCreateExtended(
        **service_schema_dict(srv_type=ServiceType.OBJECT_STORE)
    )
    assert len(srv.quotas) == 0


@parametrize_with_cases("quotas", has_tag=("service", "object-store", "quotas"))
def test_object_store_srv_create_ext_with_quotas(quotas: list[dict]) -> None:
    srv = ObjectStoreServiceCreateExtended(
        **service_schema_dict(srv_type=ServiceType.OBJECT_STORE), quotas=quotas
    )
    assert len(srv.quotas) == len(quotas)
    assert isinstance(srv.quotas[0], ObjectStoreQuotaCreateExtended)


@parametrize_with_cases("quotas", has_tag=("service", "invalid"))
def test_srv_create_ext_invalid(quotas: list[dict]) -> None:
    with pytest.raises(ValidationError, match="Multiple quotas on same project"):
        BlockStorageServiceCreateExtended(
            **service_schema_dict(srv_type=ServiceType.BLOCK_STORAGE), quotas=quotas
        )

    with pytest.raises(ValidationError, match="Multiple quotas on same project"):
        ComputeServiceCreateExtended(
            **service_schema_dict(srv_type=ServiceType.COMPUTE), quotas=quotas
        )

    with pytest.raises(ValidationError, match="Multiple quotas on same project"):
        ComputeServiceCreateExtended(
            **service_schema_dict(srv_type=ServiceType.NETWORK), quotas=quotas
        )

    with pytest.raises(ValidationError, match="Multiple quotas on same project"):
        ObjectStoreServiceCreateExtended(
            **service_schema_dict(srv_type=ServiceType.OBJECT_STORE), quotas=quotas
        )


def test_block_storage_quota_create_ext() -> None:
    project = random_lower_string()
    quota = BlockStorageQuotaCreateExtended(**quota_schema_dict(), project=project)
    assert quota.project is not None
    assert quota.project == project


def test_block_storage_quota_create_ext_invalid() -> None:
    with pytest.raises(ValidationError):
        BlockStorageQuotaCreateExtended(**quota_schema_dict())


def test_compute_quota_create_ext() -> None:
    project = random_lower_string()
    quota = ComputeQuotaCreateExtended(**quota_schema_dict(), project=project)
    assert quota.project is not None
    assert quota.project == project


def test_compute_quota_create_ext_invalid() -> None:
    with pytest.raises(ValidationError):
        ComputeQuotaCreateExtended(**quota_schema_dict())


def test_network_quota_create_ext() -> None:
    project = random_lower_string()
    quota = NetworkQuotaCreateExtended(**quota_schema_dict(), project=project)
    assert quota.project is not None
    assert quota.project == project


def test_network_quota_create_ext_invalid() -> None:
    with pytest.raises(ValidationError):
        NetworkQuotaCreateExtended(**quota_schema_dict())


def test_object_store_quota_create_ext() -> None:
    project = random_lower_string()
    quota = ObjectStoreQuotaCreateExtended(**quota_schema_dict(), project=project)
    assert quota.project is not None
    assert quota.project == project


def test_object_store_quota_create_ext_invalid() -> None:
    with pytest.raises(ValidationError):
        ObjectStoreQuotaCreateExtended(**quota_schema_dict())


@parametrize_with_cases("projects", has_tag=("flavor", "projects"))
def test_private_flavor_create_ext(projects: list[str]) -> None:
    flavor = PrivateFlavorCreateExtended(**flavor_schema_dict(), projects=projects)
    assert len(flavor.projects) > 0
    assert flavor.projects == projects


def test_private_flavor_create_ext_invalid() -> None:
    with pytest.raises(ValidationError):
        PrivateFlavorCreateExtended(**flavor_schema_dict())

    with pytest.raises(ValidationError):
        PrivateFlavorCreateExtended(**flavor_schema_dict(), projects=[])


@parametrize_with_cases("projects", has_tag=("image", "projects"))
def test_private_image_create_ext(projects: list[str]) -> None:
    image = PrivateImageCreateExtended(**image_schema_dict(), projects=projects)
    assert len(image.projects) > 0
    assert image.projects == projects


def test_private_image_create_ext_invalid() -> None:
    with pytest.raises(ValidationError):
        PrivateImageCreateExtended(**image_schema_dict())

    with pytest.raises(ValidationError):
        PrivateImageCreateExtended(**image_schema_dict(), projects=[])


@parametrize_with_cases("projects", has_tag=("network", "projects"))
def test_private_network_create_ext(projects: list[str]) -> None:
    network = PrivateNetworkCreateExtended(**network_schema_dict(), projects=projects)
    assert len(network.projects) > 0
    assert network.projects == projects


def test_private_network_create_ext_invalid() -> None:
    with pytest.raises(ValidationError):
        PrivateNetworkCreateExtended(**network_schema_dict())
