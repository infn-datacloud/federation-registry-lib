from typing import Any, List, Literal, Optional, Tuple, Union
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from pydantic import EmailStr
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from fed_reg.project.schemas import ProjectCreate, ProjectRead, ProjectReadPublic
from fed_reg.provider.enum import ProviderStatus, ProviderType
from fed_reg.provider.models import Provider
from fed_reg.provider.schemas import (
    ProviderBase,
    ProviderBasePublic,
    ProviderCreate,
    ProviderQuery,
    ProviderRead,
    ProviderReadPublic,
    ProviderUpdate,
)
from fed_reg.provider.schemas_extended import (
    BlockStorageServiceCreateExtended,
    ComputeQuotaCreateExtended,
    ComputeServiceCreateExtended,
    FlavorCreateExtended,
    IdentityProviderCreateExtended,
    IdentityProviderReadExtended,
    IdentityProviderReadExtendedPublic,
    ImageCreateExtended,
    NetworkCreateExtended,
    NetworkQuotaCreateExtended,
    NetworkServiceCreateExtended,
    ProviderCreateExtended,
    ProviderReadExtended,
    ProviderReadExtendedPublic,
    RegionCreateExtended,
    RegionReadExtended,
    RegionReadExtendedPublic,
    SLACreateExtended,
)
from tests.create_dict import (
    flavor_schema_dict,
    image_schema_dict,
    network_schema_dict,
    project_schema_dict,
    provider_schema_dict,
    region_schema_dict,
    sla_schema_dict,
)
from tests.create_model import (
    connect_provider_and_idp_neomodel,
    identity_provider_neomodel_query,
    project_neomodel_query,
    region_neomodel_query,
)
from tests.utils import random_email, random_lower_string, random_url


class CaseAttr:
    @case(tags=["base_public", "base", "update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    @case(tags=["base_public", "base"])
    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @case(tags=["base_public", "base"])
    @parametrize(value=[i for i in ProviderType])
    def case_prov_type(
        self, value: ProviderType
    ) -> Tuple[Literal["type"], ProviderType]:
        return "type", value

    @case(tags=["base"])
    @parametrize(value=[True, False])
    def case_is_public(self, value: bool) -> Tuple[Literal["is_public"], bool]:
        return "is_public", value

    @case(tags=["base"])
    @parametrize(value=[i for i in ProviderStatus])
    def case_status(
        self, value: ProviderStatus
    ) -> Tuple[Literal["status"], ProviderStatus]:
        return "status", value

    @case(tags=["base"])
    @parametrize(len=[0, 1, 2])
    def case_email_list(
        self, len: int
    ) -> Tuple[Literal["support_emails"], Optional[List[EmailStr]]]:
        attr = "support_emails"
        if len == 0:
            return attr, []
        elif len == 1:
            return attr, [random_email()]
        else:
            return attr, [random_email() for _ in range(len)]

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2])
    def case_projects(
        self, project_create_schema: ProjectCreate, len: int
    ) -> Tuple[Literal["projects"], List[ProjectCreate]]:
        if len == 1:
            return "projects", [project_create_schema]
        elif len == 2:
            return "projects", [
                project_create_schema,
                ProjectCreate(**project_schema_dict()),
            ]
        else:
            return "projects", []

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2])
    def case_regions(
        self, region_create_ext_schema: RegionCreateExtended, len: int
    ) -> Tuple[Literal["regions"], List[RegionCreateExtended]]:
        if len == 1:
            return "regions", [region_create_ext_schema]
        elif len == 2:
            return "regions", [
                region_create_ext_schema,
                RegionCreateExtended(**region_schema_dict()),
            ]
        else:
            return "regions", []

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2])
    def case_identity_providers(
        self,
        identity_provider_create_ext_schema: IdentityProviderCreateExtended,
        len: int,
    ) -> Tuple[Literal["identity_providers"], List[IdentityProviderCreateExtended]]:
        if len == 1:
            return "identity_providers", [identity_provider_create_ext_schema]
        elif len == 2:
            idp2 = identity_provider_create_ext_schema.copy()
            user_group = idp2.user_groups[0].copy()
            user_group.sla = SLACreateExtended(**sla_schema_dict(), project=uuid4())
            idp2.user_groups = [user_group]
            idp2.endpoint = random_url()
            return "identity_providers", [identity_provider_create_ext_schema, idp2]
        else:
            return "identity_providers", []


class CaseInvalidAttr:
    @case(tags=["base_public", "base", "update"])
    @parametrize(attr=["name", "type"])
    def case_attr(self, attr: str) -> Tuple[str, None]:
        return attr, None

    @case(tags=["base_public", "base"])
    def case_prov_type(self) -> Tuple[Literal["type"], str]:
        return "type", random_lower_string()

    @case(tags=["base"])
    def case_status(self) -> Tuple[Literal["status"], str]:
        return "status", random_lower_string()

    @case(tags=["base"])
    def case_email(self) -> Tuple[Literal["support_emails"], List[str]]:
        return "support_emails", [random_lower_string()]

    @case(tags=["create_extended"])
    @parametrize(attr=["name", "uuid"])
    def case_dup_projects(
        self, project_create_schema: ProjectCreate, attr: str
    ) -> Tuple[Literal["projects"], List[ProjectCreate]]:
        project2 = project_create_schema.copy()
        if attr == "name":
            project2.uuid = uuid4()
        else:
            project2.name = random_lower_string()
        return (
            "projects",
            [project_create_schema, project2],
            f"There are multiple items with identical {attr}",
        )

    @case(tags=["create_extended"])
    def case_dup_regions(
        self, region_create_ext_schema: RegionCreateExtended
    ) -> Tuple[Literal["regions"], List[RegionCreateExtended]]:
        return (
            "regions",
            [region_create_ext_schema, region_create_ext_schema],
            "There are multiple items with identical name",
        )

    @case(tags=["create_extended"])
    def case_dup_idps(
        self, identity_provider_create_ext_schema: IdentityProviderCreateExtended
    ) -> Tuple[
        Literal["identity_providers"], List[IdentityProviderCreateExtended], str
    ]:
        return (
            "identity_providers",
            [identity_provider_create_ext_schema, identity_provider_create_ext_schema],
            "There are multiple items with identical endpoint",
        )

    @case(tags=["idps"])
    def case_dup_sla_in_multi_idps(
        self, identity_provider_create_ext_schema: IdentityProviderCreateExtended
    ) -> Tuple[Literal["identity_providers"], List[ProjectCreate]]:
        idp2 = identity_provider_create_ext_schema.copy()
        idp2.endpoint = random_url()
        return (
            [identity_provider_create_ext_schema, idp2],
            "already used by another user group",
        )

    @case(tags=["idps"])
    def case_dup_project_in_multi_idps(
        self, identity_provider_create_ext_schema: IdentityProviderCreateExtended
    ) -> Tuple[Literal["identity_providers"], List[ProjectCreate]]:
        idp2 = identity_provider_create_ext_schema.copy()
        user_group = idp2.user_groups[0].copy()
        sla = user_group.sla.copy()
        sla.doc_uuid = uuid4()
        user_group.sla = sla
        idp2.user_groups = [user_group]
        idp2.endpoint = random_url()
        return (
            [identity_provider_create_ext_schema, idp2],
            "already used by another SLA",
        )

    @case(tags=["missing"])
    def case_missing_idp_projects(
        self,
        identity_provider_create_ext_schema: IdentityProviderCreateExtended,
    ) -> Tuple[
        str,
        Union[List[IdentityProviderCreateExtended], List[RegionCreateExtended]],
        Literal["not in this provider"],
    ]:
        return (
            "identity_providers",
            [identity_provider_create_ext_schema],
            "not in this provider",
        )

    @case(tags=["missing"])
    def case_missing_block_storage_projects(
        self,
        region_create_ext_schema: RegionCreateExtended,
        block_storage_service_create_ext_schema: BlockStorageServiceCreateExtended,
        block_storage_quota_create_ext_schema: BlockStorageServiceCreateExtended,
    ) -> Tuple[
        str,
        Union[List[IdentityProviderCreateExtended], List[RegionCreateExtended]],
        Literal["not in this provider"],
    ]:
        block_storage_service_create_ext_schema.quotas = [
            block_storage_quota_create_ext_schema
        ]
        region_create_ext_schema.block_storage_services = [
            block_storage_service_create_ext_schema
        ]
        return ("regions", [region_create_ext_schema], "not in this provider")

    @case(tags=["missing"])
    @parametrize(resource=["quotas", "flavors", "images"])
    def case_missing_compute_projects(
        self,
        region_create_ext_schema: RegionCreateExtended,
        compute_service_create_ext_schema: ComputeServiceCreateExtended,
        compute_quota_create_ext_schema: ComputeQuotaCreateExtended,
        resource: str,
    ) -> Tuple[
        str,
        Union[List[IdentityProviderCreateExtended], List[RegionCreateExtended]],
        Literal["not in this provider"],
    ]:
        if resource == "quotas":
            compute_service_create_ext_schema.quotas = [compute_quota_create_ext_schema]
        elif resource == "flavors":
            item = FlavorCreateExtended(
                **flavor_schema_dict(), is_public=False, projects=[uuid4()]
            )
            compute_service_create_ext_schema.flavors = [item]
        elif resource == "images":
            item = ImageCreateExtended(
                **image_schema_dict(), is_public=False, projects=[uuid4()]
            )
            compute_service_create_ext_schema.images = [item]
        region_create_ext_schema.compute_services = [compute_service_create_ext_schema]
        return ("regions", [region_create_ext_schema], "not in this provider")

    @case(tags=["missing"])
    @parametrize(resource=["quotas", "networks"])
    def case_missing_network_projects(
        self,
        region_create_ext_schema: RegionCreateExtended,
        network_service_create_ext_schema: NetworkServiceCreateExtended,
        network_quota_create_ext_schema: NetworkQuotaCreateExtended,
        resource: str,
    ) -> Tuple[
        str,
        Union[List[IdentityProviderCreateExtended], List[RegionCreateExtended]],
        Literal["not in this provider"],
    ]:
        if resource == "quotas":
            network_service_create_ext_schema.quotas = [network_quota_create_ext_schema]
        elif resource == "networks":
            item = NetworkCreateExtended(
                **network_schema_dict(), is_shared=False, project=uuid4()
            )
            network_service_create_ext_schema.networks = [item]
        region_create_ext_schema.network_services = [network_service_create_ext_schema]
        return ("regions", [region_create_ext_schema], "not in this provider")


class CaseDBInstance:
    @case(tags=["provider"])
    @parametrize(tot_proj=[0, 1, 2])
    @parametrize(tot_reg=[0, 1, 2])
    @parametrize(tot_idp=[0, 1, 2])
    def case_provider(
        self,
        db_core: MagicMock,
        db_match: MagicMock,
        db_rel_mgr: MagicMock,
        provider_model: Provider,
        tot_proj: int,
        tot_reg: int,
        tot_idp: int,
    ) -> Provider:
        def query_call(query, params, **kwargs) -> Tuple[List, None]:
            """Mock function to emulate cypher query.

            Response changes based on parametrized value and on executed query.
            """
            if "identity_providers_r1" in query:
                items, rels = identity_provider_neomodel_query(tot_idp, db_core)
                for item in items:
                    connect_provider_and_idp_neomodel(
                        db_core, provider=provider_model, identity_provider=item[0]
                    )
                return items, rels
            if "projects_r1" in query:
                return project_neomodel_query(tot_proj, db_core)
            if "regions_r1" in query:
                return region_neomodel_query(tot_reg, db_core)
            return ([], None)

        db_match.cypher_query.side_effect = query_call

        return provider_model


class CasePublic:
    @parametrize(is_public=[True, False])
    def case_public(self, is_public: bool):
        return is_public


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_base_public(key: str, value: str) -> None:
    assert issubclass(ProviderBasePublic, BaseNode)
    d = provider_schema_dict()
    if key:
        d[key] = value
    item = ProviderBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.name == d.get("name")
    assert item.type == d.get("type").value


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_base_public(key: str, value: None) -> None:
    d = provider_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ProviderBasePublic(**d)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base"])
def test_base(key: str, value: Any) -> None:
    assert issubclass(ProviderBase, ProviderBasePublic)
    d = provider_schema_dict()
    if key:
        d[key] = value
    item = ProviderBase(**d)
    assert item.name == d.get("name")
    assert item.type == d.get("type").value
    assert item.status == d.get("status", ProviderStatus.ACTIVE).value
    assert item.is_public == d.get("is_public", False)
    assert item.support_emails == d.get("support_emails", [])


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base"])
def test_invalid_base(key: str, value: Any) -> None:
    d = provider_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ProviderBase(**d)


def test_create() -> None:
    assert issubclass(ProviderCreate, BaseNodeCreate)
    assert issubclass(ProviderCreate, ProviderBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(ProviderUpdate, BaseNodeCreate)
    assert issubclass(ProviderUpdate, ProviderBase)
    d = provider_schema_dict()
    if key:
        d[key] = value
    item = ProviderUpdate(**d)
    assert item.name == d.get("name")
    assert item.type == (d.get("type").value if d.get("type") else None)


def test_query() -> None:
    assert issubclass(ProviderQuery, BaseNodeQuery)


@parametrize_with_cases("attr, values", cases=CaseAttr, has_tag=["create_extended"])
def test_create_extended(
    attr: str,
    values: Optional[
        Union[
            List[IdentityProviderCreateExtended],
            List[ProjectCreate],
            List[RegionCreateExtended],
        ]
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


@parametrize_with_cases(
    "attr, values, msg", cases=CaseInvalidAttr, has_tag=["create_extended"]
)
def test_invalid_create_extended(
    attr: str,
    values: Union[
        List[IdentityProviderCreateExtended],
        List[ProjectCreate],
        List[RegionCreateExtended],
    ],
    msg: str,
) -> None:
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
    with pytest.raises(ValueError, match=msg):
        ProviderCreateExtended(**d)


@parametrize_with_cases(
    "identity_providers, msg", cases=CaseInvalidAttr, has_tag=["idps"]
)
def test_dup_proj_in_idps_in_create_extended(
    identity_providers: Union[
        List[IdentityProviderCreateExtended],
        List[ProjectCreate],
        List[RegionCreateExtended],
    ],
    msg: str,
) -> None:
    d = provider_schema_dict()
    d["identity_providers"] = identity_providers
    projects = set()
    for idp in identity_providers:
        for user_group in idp.user_groups:
            projects.add(user_group.sla.project)
    d["projects"] = [
        ProjectCreate(name=random_lower_string(), uuid=p) for p in projects
    ]
    with pytest.raises(ValueError, match=msg):
        ProviderCreateExtended(**d)


@parametrize_with_cases("attr, values, msg", cases=CaseInvalidAttr, has_tag=["missing"])
def test_miss_proj_in_idps_in_create_extended(
    attr: str,
    values: Union[List[IdentityProviderCreateExtended], List[RegionCreateExtended]],
    msg: str,
) -> None:
    d = provider_schema_dict()
    d[attr] = values
    with pytest.raises(ValueError, match=msg):
        ProviderCreateExtended(**d)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_read_public(provider_model: Provider, key: str, value: str) -> None:
    assert issubclass(ProviderReadPublic, ProviderBasePublic)
    assert issubclass(ProviderReadPublic, BaseNodeRead)
    assert ProviderReadPublic.__config__.orm_mode

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


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_read_public(provider_model: Provider, key: str, value: str) -> None:
    provider_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ProviderReadPublic.from_orm(provider_model)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base"])
def test_read(provider_model: Provider, key: str, value: Any) -> None:
    assert issubclass(ProviderRead, ProviderBase)
    assert issubclass(ProviderRead, BaseNodeRead)
    assert ProviderRead.__config__.orm_mode

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


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base"])
def test_invalid_read(provider_model: Provider, key: str, value: str) -> None:
    provider_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ProviderRead.from_orm(provider_model)


@parametrize_with_cases("model", cases=CaseDBInstance, has_tag="provider")
@parametrize_with_cases("public", cases=CasePublic)
def test_read_extended(model: Provider, public: bool) -> None:
    if public:
        cls = ProviderReadPublic
        cls_ext = ProviderReadExtendedPublic
        idp_cls = IdentityProviderReadExtendedPublic
        reg_cls = RegionReadExtendedPublic
        proj_cls = ProjectReadPublic
    else:
        cls = ProviderRead
        cls_ext = ProviderReadExtended
        idp_cls = IdentityProviderReadExtended
        reg_cls = RegionReadExtended
        proj_cls = ProjectRead

    assert issubclass(cls_ext, cls)
    assert cls_ext.__config__.orm_mode

    item = cls_ext.from_orm(model)

    assert len(item.identity_providers) == len(model.identity_providers.all())
    assert len(item.projects) == len(model.projects.all())
    assert len(item.regions) == len(model.regions.all())

    assert all([isinstance(i, idp_cls) for i in item.identity_providers])
    assert all([isinstance(i, proj_cls) for i in item.projects])
    assert all([isinstance(i, reg_cls) for i in item.regions])
