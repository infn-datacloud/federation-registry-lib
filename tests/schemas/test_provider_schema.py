from typing import Any, Optional

from pytest_cases import parametrize_with_cases

from fed_reg.project.schemas import ProjectCreate
from fed_reg.provider.enum import ProviderStatus, ProviderType
from fed_reg.provider.models import Provider
from fed_reg.provider.schemas import (
    ProviderBase,
    ProviderBasePublic,
    ProviderCreate,
    ProviderRead,
    ProviderReadPublic,
    ProviderUpdate,
)
from fed_reg.provider.schemas_extended import (
    IdentityProviderCreateExtended,
    ProviderCreateExtended,
    RegionCreateExtended,
)
from tests.create_dict import (
    provider_schema_dict,
)
from tests.utils import random_lower_string


@parametrize_with_cases("key, value", has_tag="base_public")
def test_base_public(key: str, value: str) -> None:
    d = provider_schema_dict()
    if key:
        d[key] = value
    item = ProviderBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")
    assert item.type == d.get("type").value


@parametrize_with_cases("key, value", has_tag="base")
def test_base(key: str, value: Any) -> None:
    d = provider_schema_dict()
    if key:
        d[key] = value
    item = ProviderBase(**d)
    assert item.name == d.get("name")
    assert item.type == d.get("type").value
    assert item.status == d.get("status", ProviderStatus.ACTIVE).value
    assert item.is_public == d.get("is_public", False)
    assert item.support_emails == d.get("support_emails", [])


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(provider_model: Provider, key: str, value: str) -> None:
    if key:
        if isinstance(value, ProviderType):
            value = value.value
        provider_model.__setattr__(key, value)
    item = ProviderReadPublic.from_orm(provider_model)

    assert item.uid
    assert item.uid == provider_model.uid
    assert item.description == provider_model.description
    assert item.name == provider_model.name
    assert item.type == provider_model.type


@parametrize_with_cases("key, value", has_tag="base")
def test_read(provider_model: Provider, key: str, value: Any) -> None:
    if key:
        if isinstance(value, (ProviderType, ProviderStatus)):
            value = value.value
        provider_model.__setattr__(key, value)
    item = ProviderRead.from_orm(provider_model)

    assert item.uid
    assert item.uid == provider_model.uid
    assert item.description == provider_model.description
    assert item.name == provider_model.name
    assert item.type == provider_model.type
    if provider_model.status:
        assert item.status == provider_model.status
    else:
        assert item.status == ProviderStatus.ACTIVE.value
    assert item.is_public == provider_model.is_public
    assert item.support_emails == provider_model.support_emails


@parametrize_with_cases("attr, values", has_tag="create_extended")
def test_create_extended(
    attr: str,
    values: Optional[
        list[IdentityProviderCreateExtended]
        | list[ProjectCreate]
        | list[RegionCreateExtended]
    ],
) -> None:
    assert issubclass(ProviderCreateExtended, ProviderCreate)
    d = provider_schema_dict()
    d[attr] = values
    if attr == "identity_providers":
        projects = set()
        for idp in values:
            for user_group in idp.user_groups:
                projects.add(user_group.sla.project)
        d["projects"] = [
            ProjectCreate(name=random_lower_string(), uuid=p) for p in projects
        ]
    item = ProviderCreateExtended(**d)
    assert item.__getattribute__(attr) == values


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = provider_schema_dict()
    if key:
        d[key] = value
    item = ProviderUpdate(**d)
    assert item.name == d.get("name")
    assert item.type == (d.get("type").value if d.get("type") else None)


# @parametrize_with_cases("model", cases=CaseDBInstance, has_tag="provider")
# @parametrize_with_cases("public", cases=CasePublic)
# def test_read_extended(model: Provider, public: bool) -> None:
#     if public:
#         cls = ProviderReadPublic
#         cls_ext = ProviderReadExtendedPublic
#         idp_cls = IdentityProviderReadExtendedPublic
#         reg_cls = RegionReadExtendedPublic
#         proj_cls = ProjectReadPublic
#     else:
#         cls = ProviderRead
#         cls_ext = ProviderReadExtended
#         idp_cls = IdentityProviderReadExtended
#         reg_cls = RegionReadExtended
#         proj_cls = ProjectRead

#     assert issubclass(cls_ext, cls)
#     assert cls_ext.__config__.orm_mode

#     item = cls_ext.from_orm(model)

#     assert len(item.identity_providers) == len(model.identity_providers.all())
#     assert len(item.projects) == len(model.projects.all())
#     assert len(item.regions) == len(model.regions.all())

#     assert all([isinstance(i, idp_cls) for i in item.identity_providers])
#     assert all([isinstance(i, proj_cls) for i in item.projects])
#     assert all([isinstance(i, reg_cls) for i in item.regions])


# @parametrize_with_cases("model", cases=CaseDBInstance, has_tag="region")
# @parametrize_with_cases("public", cases=CasePublic)
# def test_read_extended_subclass_region(model: Region, public: bool) -> None:
#     if public:
#         cls = RegionReadPublic
#         cls_ext = RegionReadExtendedPublic
#         loc_cls = LocationReadPublic
#         bsto_srv_cls = BlockStorageServiceReadExtendedPublic
#         comp_srv_cls = ComputeServiceReadExtendedPublic
#         id_srv_cls = IdentityServiceReadPublic
#         net_srv_cls = NetworkServiceReadExtendedPublic
#     else:
#         cls = RegionRead
#         cls_ext = RegionReadExtended
#         loc_cls = LocationRead
#         bsto_srv_cls = BlockStorageServiceReadExtended
#         comp_srv_cls = ComputeServiceReadExtended
#         id_srv_cls = IdentityServiceRead
#         net_srv_cls = NetworkServiceReadExtended

#     assert issubclass(cls_ext, cls)
#     assert cls_ext.__config__.orm_mode

#     item = cls_ext.from_orm(model)

#     if not item.location:
#         assert not len(model.location.all())
#         assert not model.location.single()
#     else:
#         assert len(model.location.all()) == 1
#         assert model.location.single()
#     assert len(item.services) == len(model.services.all())

#     if item.location:
#         assert isinstance(item.location, loc_cls)
#     assert all(
#         [
#             isinstance(i, (bsto_srv_cls, comp_srv_cls, id_srv_cls, net_srv_cls))
#             for i in item.services
#         ]
#     )


# @parametrize_with_cases("model", cases=CaseDBInstance, has_tag="identity_provider")
# @parametrize_with_cases("public", cases=CasePublic)
# def test_read_extended_subclass_identity_provider(
#     model: Provider, public: bool
# ) -> None:
#     if public:
#         cls = IdentityProviderReadPublic
#         cls_ext = IdentityProviderReadExtendedPublic
#         prov_cls = ProviderReadExtendedPublic
#         group_cls = UserGroupReadExtendedPublic
#     else:
#         cls = IdentityProviderRead
#         cls_ext = IdentityProviderReadExtended
#         prov_cls = ProviderReadExtended
#         group_cls = UserGroupReadExtended

#     assert issubclass(cls_ext, cls)
#     assert cls_ext.__config__.orm_mode

#     item = prov_cls.from_orm(model)

#     model = model.identity_providers.single()
#     item = item.identity_providers[0]

#     assert item.relationship is not None

#     assert len(item.user_groups) == len(model.user_groups.all())

#     assert all([isinstance(i, group_cls) for i in item.user_groups])


# @parametrize_with_cases("model", cases=CaseDBInstance, has_tag="user_group")
# @parametrize_with_cases("public", cases=CasePublic)
# def test_read_extended_subclass_user_groups(model: UserGroup, public: bool) -> None:
#     if public:
#         cls = UserGroupReadPublic
#         cls_ext = UserGroupReadExtendedPublic
#         sla_cls = SLAReadPublic
#     else:
#         cls = UserGroupRead
#         cls_ext = UserGroupReadExtended
#         sla_cls = SLARead

#     assert issubclass(cls_ext, cls)
#     assert cls_ext.__config__.orm_mode

#     item = cls_ext.from_orm(model)

#     assert len(item.slas) == len(model.slas.all())

#     assert all([isinstance(i, sla_cls) for i in item.slas])


# @parametrize_with_cases("model", cases=CaseDBInstance,
#   has_tag="block_storage_service")
# @parametrize_with_cases("public", cases=CasePublic)
# def test_read_extended_subclass_block_storage_service(
#     model: BlockStorageService, public: bool
# ) -> None:
#     if public:
#         cls = BlockStorageServiceReadPublic
#         cls_ext = BlockStorageServiceReadExtendedPublic
#         quota_cls = BlockStorageQuotaReadPublic
#     else:
#         cls = BlockStorageServiceRead
#         cls_ext = BlockStorageServiceReadExtended
#         quota_cls = BlockStorageQuotaRead

#     assert issubclass(cls_ext, cls)
#     assert cls_ext.__config__.orm_mode

#     item = cls_ext.from_orm(model)

#     assert len(item.quotas) == len(model.quotas.all())

#     assert all([isinstance(i, quota_cls) for i in item.quotas])


# @parametrize_with_cases("model", cases=CaseDBInstance, has_tag="compute_service")
# @parametrize_with_cases("public", cases=CasePublic)
# def test_read_extended_subclass_compute_service(
#     model: ComputeService, public: bool
# ) -> None:
#     if public:
#         cls = ComputeServiceReadPublic
#         cls_ext = ComputeServiceReadExtendedPublic
#         flavor_cls = FlavorReadPublic
#         image_cls = ImageReadPublic
#         quota_cls = ComputeQuotaReadPublic
#     else:
#         cls = ComputeServiceRead
#         cls_ext = ComputeServiceReadExtended
#         flavor_cls = FlavorRead
#         image_cls = ImageRead
#         quota_cls = ComputeQuotaRead

#     assert issubclass(cls_ext, cls)
#     assert cls_ext.__config__.orm_mode

#     item = cls_ext.from_orm(model)

#     assert len(item.flavors) == len(model.flavors.all())
#     assert len(item.images) == len(model.images.all())
#     assert len(item.quotas) == len(model.quotas.all())

#     assert all([isinstance(i, flavor_cls) for i in item.flavors])
#     assert all([isinstance(i, image_cls) for i in item.images])
#     assert all([isinstance(i, quota_cls) for i in item.quotas])


# @parametrize_with_cases("model", cases=CaseDBInstance, has_tag="network_service")
# @parametrize_with_cases("public", cases=CasePublic)
# def test_read_extended_subclass_network_service(
#     model: NetworkService, public: bool
# ) -> None:
#     if public:
#         cls = NetworkServiceReadPublic
#         cls_ext = NetworkServiceReadExtendedPublic
#         net_cls = NetworkReadPublic
#         quota_cls = NetworkQuotaReadPublic
#     else:
#         cls = NetworkServiceRead
#         cls_ext = NetworkServiceReadExtended
#         net_cls = NetworkRead
#         quota_cls = NetworkQuotaRead

#     assert issubclass(cls_ext, cls)
#     assert cls_ext.__config__.orm_mode

#     item = cls_ext.from_orm(model)

#     assert len(item.networks) == len(model.networks.all())
#     assert len(item.quotas) == len(model.quotas.all())

#     assert all([isinstance(i, net_cls) for i in item.networks])
#     assert all([isinstance(i, quota_cls) for i in item.quotas])
