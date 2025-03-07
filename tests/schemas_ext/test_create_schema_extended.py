import pytest
from pydantic import BaseModel, Field, ValidationError
from pytest_cases import parametrize_with_cases

from fedreg.flavor.schemas import PrivateFlavorCreate
from fedreg.identity_provider.schemas import IdentityProviderCreate
from fedreg.image.schemas import PrivateImageCreate
from fedreg.location.schemas import LocationCreate
from fedreg.network.schemas import PrivateNetworkCreate
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
    find_duplicate_projects,
    find_duplicate_slas,
    find_duplicates,
    multiple_quotas_same_project,
)
from fedreg.quota.schemas import (
    BlockStorageQuotaCreate,
    ComputeQuotaCreate,
    NetworkQuotaCreate,
    ObjectStoreQuotaCreate,
    QuotaBase,
)
from fedreg.region.schemas import RegionCreate
from fedreg.service.schemas import (
    BlockStorageServiceCreate,
    ComputeServiceCreate,
    NetworkServiceCreate,
    ObjectStoreServiceCreate,
)
from fedreg.sla.schemas import SLACreate
from fedreg.user_group.schemas import UserGroupCreate
from tests.schemas.utils import provider_schema_dict, region_schema_dict
from tests.utils import random_lower_string


class TestModel(BaseModel):
    __test__ = False
    test_field: str = Field(decription="Test field")


class TestQuota(QuotaBase):
    __test__ = False
    project: str = Field(description="Project field")


def test_find_duplicates() -> None:
    a = "str1"
    b = "str2"
    find_duplicates([a, b])

    a = "str1"
    b = "str1"
    with pytest.raises(
        AssertionError, match=f"There are multiple identical items: {a}"
    ):
        find_duplicates([a, b])

    a = TestModel(test_field="str1")
    b = TestModel(test_field="str2")
    find_duplicates([a, b], attr="test_field")

    a = TestModel(test_field="str1")
    b = TestModel(test_field="str1")
    with pytest.raises(
        AssertionError,
        match=f"There are multiple items with identical test_field: {a.test_field}",
    ):
        find_duplicates([a, b], attr="test_field")


def test_multiple_quotas() -> None:
    project = "project1"
    q1 = TestQuota(project=project)
    multiple_quotas_same_project([q1])
    q2 = TestQuota(project=project, per_user=True)
    multiple_quotas_same_project([q1, q2])
    q3 = TestQuota(project=project, usage=True)
    multiple_quotas_same_project([q1, q2, q3])

    q4 = TestQuota(project="project2")
    multiple_quotas_same_project([q1, q2, q4])
    q4 = TestQuota(project="project2", per_user=True)
    multiple_quotas_same_project([q1, q2, q4])
    q4 = TestQuota(project="project2", usage=True)
    multiple_quotas_same_project([q1, q2, q4])

    q4 = TestQuota(project=project)
    with pytest.raises(
        AssertionError, match=f"Multiple quotas on same project {project}"
    ):
        multiple_quotas_same_project([q1, q2, q3, q4])

    q4 = TestQuota(project=project, per_user=True)
    with pytest.raises(
        AssertionError, match=f"Multiple quotas on same project {project}"
    ):
        multiple_quotas_same_project([q1, q2, q3, q4])

    q4 = TestQuota(project=project, usage=True)
    with pytest.raises(
        AssertionError, match=f"Multiple quotas on same project {project}"
    ):
        multiple_quotas_same_project([q1, q2, q3, q4])


def test_find_dup_proj() -> None:
    s = set(["project1"])
    find_duplicate_projects("project2", s)
    assert len(s) == 2

    s = set(["project1"])
    with pytest.raises(
        AssertionError, match="Project project1 already used by another SLA"
    ):
        find_duplicate_projects("project1", s)
    assert len(s) == 1


def test_find_dup_sla() -> None:
    s = set(["sla1"])
    find_duplicate_slas("sla2", s)
    assert len(s) == 2

    s = set(["sla1"])
    with pytest.raises(
        AssertionError, match="SLA sla1 already used by another user group"
    ):
        find_duplicate_slas("sla1", s)
    assert len(s) == 1


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
    assert len(idp.user_groups) == len(identity_provider["user_groups"])
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
    assert item.sla is not None
    assert isinstance(item.sla, SLACreateExtended)


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


# from fedreg.provider.schemas_extended import (
#     IdentityProviderCreateExtended,
#     ProjectCreate,
#     ProviderCreateExtended,
#     RegionCreateExtended,
# )
# from tests.schemas.utils import provider_schema_dict
# from tests.utils import random_lower_string


# # @parametrize_with_cases("projects", has_tag="create_extended")
# # def test_create_private_extended(projects: list[UUID]) -> None:
# #     d = flavor_schema_dict()
# #     d["projects"] = projects
# #     item = PrivateFlavorCreateExtended(**d)
# #     assert item.projects == [i.hex for i in projects]

# # @parametrize_with_cases("projects", has_tag="create_extended")
# # def test_invalid_create_private_extended(projects: list[UUID]) -> None:
# #     d = flavor_schema_dict()
# #     with pytest.raises(ValidationError):
# #         PrivateFlavorCreateExtended(**d)
# #     with pytest.raises(ValidationError):
# #         PrivateFlavorCreateExtended(**d, projects=projects, is_shared=True)


# # def test_create_shared_extended(projects: list[UUID]) -> None:
# #     d = flavor_schema_dict()
# #     SharedFlavorCreateExtended(**d)
# #     # Even if we pass projects they are discarded
# #     item = SharedFlavorCreateExtended(**d, projects=projects)
# #     with pytest.raises(AttributeError):
# #         item.__getattribute__("projects")


# # def test_invalid_create_shared_extended() -> None:
# #     d = flavor_schema_dict()
# #     with pytest.raises(ValidationError):
# #         SharedFlavorCreateExtended(**d, is_shared=False)

# @parametrize_with_cases("attr, values", has_tag="valid")
# def test_create_extended(
#     attr: str,
#     values: list[IdentityProviderCreateExtended]
#     | list[ProjectCreate]
#     | list[RegionCreateExtended],
# ) -> None:
#     d = provider_schema_dict()
#     d[attr] = values
#     if attr == "identity_providers":
#         projects = set()
#         for idp in values:
#             for user_group in idp.user_groups:
#                 projects.add(user_group.sla.sla)
#         d["projects"] = [
#             ProjectCreate(name=random_lower_string(), uuid=p) for p in projects
#         ]
#     item = ProviderCreateExtended(**d)
#     assert item.__getattribute__(attr) == values


# @parametrize_with_cases("attr, values, msg", has_tag="invalid")
# def test_invalid_create_extended(
#     attr: str,
#     values: list[IdentityProviderCreateExtended]
#     | list[ProjectCreate]
#     | list[RegionCreateExtended],
#     msg: str,
# ) -> None:
#     d = provider_schema_dict()
#     d[attr] = values
#     if attr == "identity_providers":
#         projects = set()
#         for idp in values:
#             for user_group in idp.user_groups:
#                 projects.add(user_group.sla.project)
#         d["projects"] = [
#             ProjectCreate(name=random_lower_string(), uuid=p) for p in projects
#         ]
#     with pytest.raises(ValueError, match=msg):
#         ProviderCreateExtended(**d)


# @parametrize_with_cases("identity_providers, msg", has_tag="idps")
# def test_dup_proj_in_idps_in_create_extended(
#     identity_providers: list[IdentityProviderCreateExtended]
#     | list[ProjectCreate]
#     | list[RegionCreateExtended],
#     msg: str,
# ) -> None:
#     d = provider_schema_dict()
#     d["identity_providers"] = identity_providers
#     projects = set()
#     for idp in identity_providers:
#         for user_group in idp.user_groups:
#             projects.add(user_group.sla.project)
#     d["projects"] = [
#         ProjectCreate(name=random_lower_string(), uuid=p) for p in projects
#     ]
#     with pytest.raises(ValueError, match=msg):
#         ProviderCreateExtended(**d)


# @parametrize_with_cases("attr, values, msg", has_tag="missing")
# def test_miss_proj_in_idps_in_create_extended(
#     attr: str,
#     values: list[IdentityProviderCreateExtended] | list[RegionCreateExtended],
#     msg: str,
# ) -> None:
#     d = provider_schema_dict()
#     d[attr] = values
#     with pytest.raises(ValueError, match=msg):
#         ProviderCreateExtended(**d)


# # @parametrize_with_cases("model", cases=CaseDBInstance, has_tag="provider")
# # @parametrize_with_cases("public", cases=CasePublic)
# # def test_read_extended(model: Provider, public: bool) -> None:
# #     if public:
# #         cls = ProviderReadPublic
# #         cls_ext = ProviderReadExtendedPublic
# #         idp_cls = IdentityProviderReadExtendedPublic
# #         reg_cls = RegionReadExtendedPublic
# #         proj_cls = ProjectReadPublic
# #     else:
# #         cls = ProviderRead
# #         cls_ext = ProviderReadExtended
# #         idp_cls = IdentityProviderReadExtended
# #         reg_cls = RegionReadExtended
# #         proj_cls = ProjectRead

# #     assert issubclass(cls_ext, cls)
# #     assert cls_ext.__config__.orm_mode

# #     item = cls_ext.from_orm(model)

# #     assert len(item.identity_providers) == len(model.identity_providers.all())
# #     assert len(item.projects) == len(model.projects.all())
# #     assert len(item.regions) == len(model.regions.all())

# #     assert all([isinstance(i, idp_cls) for i in item.identity_providers])
# #     assert all([isinstance(i, proj_cls) for i in item.projects])
# #     assert all([isinstance(i, reg_cls) for i in item.regions])


# # @parametrize_with_cases("model", cases=CaseDBInstance, has_tag="region")
# # @parametrize_with_cases("public", cases=CasePublic)
# # def test_read_extended_subclass_region(model: Region, public: bool) -> None:
# #     if public:
# #         cls = RegionReadPublic
# #         cls_ext = RegionReadExtendedPublic
# #         loc_cls = LocationReadPublic
# #         bsto_srv_cls = BlockStorageServiceReadExtendedPublic
# #         comp_srv_cls = ComputeServiceReadExtendedPublic
# #         id_srv_cls = IdentityServiceReadPublic
# #         net_srv_cls = NetworkServiceReadExtendedPublic
# #     else:
# #         cls = RegionRead
# #         cls_ext = RegionReadExtended
# #         loc_cls = LocationRead
# #         bsto_srv_cls = BlockStorageServiceReadExtended
# #         comp_srv_cls = ComputeServiceReadExtended
# #         id_srv_cls = IdentityServiceRead
# #         net_srv_cls = NetworkServiceReadExtended

# #     assert issubclass(cls_ext, cls)
# #     assert cls_ext.__config__.orm_mode

# #     item = cls_ext.from_orm(model)

# #     if not item.location:
# #         assert not len(model.location.all())
# #         assert not model.location.single()
# #     else:
# #         assert len(model.location.all()) == 1
# #         assert model.location.single()
# #     assert len(item.services) == len(model.services.all())

# #     if item.location:
# #         assert isinstance(item.location, loc_cls)
# #     assert all(
# #         [
# #             isinstance(i, (bsto_srv_cls, comp_srv_cls, id_srv_cls, net_srv_cls))
# #             for i in item.services
# #         ]
# #     )


# # @parametrize_with_cases("model", cases=CaseDBInstance, has_tag="identity_provider")
# # @parametrize_with_cases("public", cases=CasePublic)
# # def test_read_extended_subclass_identity_provider(
# #     model: Provider, public: bool
# # ) -> None:
# #     if public:
# #         cls = IdentityProviderReadPublic
# #         cls_ext = IdentityProviderReadExtendedPublic
# #         prov_cls = ProviderReadExtendedPublic
# #         group_cls = UserGroupReadExtendedPublic
# #     else:
# #         cls = IdentityProviderRead
# #         cls_ext = IdentityProviderReadExtended
# #         prov_cls = ProviderReadExtended
# #         group_cls = UserGroupReadExtended

# #     assert issubclass(cls_ext, cls)
# #     assert cls_ext.__config__.orm_mode

# #     item = prov_cls.from_orm(model)

# #     model = model.identity_providers.single()
# #     item = item.identity_providers[0]

# #     assert item.relationship is not None

# #     assert len(item.user_groups) == len(model.user_groups.all())

# #     assert all([isinstance(i, group_cls) for i in item.user_groups])


# # @parametrize_with_cases("model", cases=CaseDBInstance, has_tag="user_group")
# # @parametrize_with_cases("public", cases=CasePublic)
# # def test_read_extended_subclass_user_groups(model: UserGroup, public: bool) -> None:
# #     if public:
# #         cls = UserGroupReadPublic
# #         cls_ext = UserGroupReadExtendedPublic
# #         sla_cls = SLAReadPublic
# #     else:
# #         cls = UserGroupRead
# #         cls_ext = UserGroupReadExtended
# #         sla_cls = SLARead

# #     assert issubclass(cls_ext, cls)
# #     assert cls_ext.__config__.orm_mode

# #     item = cls_ext.from_orm(model)

# #     assert len(item.slas) == len(model.slas.all())

# #     assert all([isinstance(i, sla_cls) for i in item.slas])


# # @parametrize_with_cases("model", cases=CaseDBInstance,
# #   has_tag="block_storage_service")
# # @parametrize_with_cases("public", cases=CasePublic)
# # def test_read_extended_subclass_block_storage_service(
# #     model: BlockStorageService, public: bool
# # ) -> None:
# #     if public:
# #         cls = BlockStorageServiceReadPublic
# #         cls_ext = BlockStorageServiceReadExtendedPublic
# #         quota_cls = BlockStorageQuotaReadPublic
# #     else:
# #         cls = BlockStorageServiceRead
# #         cls_ext = BlockStorageServiceReadExtended
# #         quota_cls = BlockStorageQuotaRead

# #     assert issubclass(cls_ext, cls)
# #     assert cls_ext.__config__.orm_mode

# #     item = cls_ext.from_orm(model)

# #     assert len(item.quotas) == len(model.quotas.all())

# #     assert all([isinstance(i, quota_cls) for i in item.quotas])


# # @parametrize_with_cases("model", cases=CaseDBInstance, has_tag="compute_service")
# # @parametrize_with_cases("public", cases=CasePublic)
# # def test_read_extended_subclass_compute_service(
# #     model: ComputeService, public: bool
# # ) -> None:
# #     if public:
# #         cls = ComputeServiceReadPublic
# #         cls_ext = ComputeServiceReadExtendedPublic
# #         flavor_cls = FlavorReadPublic
# #         image_cls = ImageReadPublic
# #         quota_cls = ComputeQuotaReadPublic
# #     else:
# #         cls = ComputeServiceRead
# #         cls_ext = ComputeServiceReadExtended
# #         flavor_cls = FlavorRead
# #         image_cls = ImageRead
# #         quota_cls = ComputeQuotaRead

# #     assert issubclass(cls_ext, cls)
# #     assert cls_ext.__config__.orm_mode

# #     item = cls_ext.from_orm(model)

# #     assert len(item.flavors) == len(model.flavors.all())
# #     assert len(item.images) == len(model.images.all())
# #     assert len(item.quotas) == len(model.quotas.all())

# #     assert all([isinstance(i, flavor_cls) for i in item.flavors])
# #     assert all([isinstance(i, image_cls) for i in item.images])
# #     assert all([isinstance(i, quota_cls) for i in item.quotas])


# # @parametrize_with_cases("model", cases=CaseDBInstance, has_tag="network_service")
# # @parametrize_with_cases("public", cases=CasePublic)
# # def test_read_extended_subclass_network_service(
# #     model: NetworkService, public: bool
# # ) -> None:
# #     if public:
# #         cls = NetworkServiceReadPublic
# #         cls_ext = NetworkServiceReadExtendedPublic
# #         net_cls = NetworkReadPublic
# #         quota_cls = NetworkQuotaReadPublic
# #     else:
# #         cls = NetworkServiceRead
# #         cls_ext = NetworkServiceReadExtended
# #         net_cls = NetworkRead
# #         quota_cls = NetworkQuotaRead

# #     assert issubclass(cls_ext, cls)
# #     assert cls_ext.__config__.orm_mode

# #     item = cls_ext.from_orm(model)

# #     assert len(item.networks) == len(model.networks.all())
# #     assert len(item.quotas) == len(model.quotas.all())

# #     assert all([isinstance(i, net_cls) for i in item.networks])
# #     assert all([isinstance(i, quota_cls) for i in item.quotas])
