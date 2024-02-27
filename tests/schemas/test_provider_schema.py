from typing import Any, List, Literal, Optional, Tuple, Union
from uuid import uuid4

import pytest
from pydantic import EmailStr
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery
from fed_reg.project.schemas import ProjectCreate
from fed_reg.provider.enum import ProviderStatus, ProviderType
from fed_reg.provider.schemas import (
    ProviderBase,
    ProviderBasePublic,
    ProviderCreate,
    ProviderQuery,
    ProviderUpdate,
)
from fed_reg.provider.schemas_extended import (
    IdentityProviderCreateExtended,
    ProviderCreateExtended,
    RegionCreateExtended,
    SLACreateExtended,
    UserGroupCreateExtended,
)
from tests.create_dict import (
    auth_method_dict,
    identity_provider_schema_dict,
    project_schema_dict,
    provider_schema_dict,
    region_schema_dict,
    sla_schema_dict,
    user_group_schema_dict,
)
from tests.utils import random_email, random_lower_string


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @case(tags=["base_public"])
    @parametrize(value=[i for i in ProviderType])
    def case_type(self, value: ProviderType) -> Tuple[Literal["type"], ProviderType]:
        return "type", value

    @parametrize(value=[True, False])
    def case_is_public(self, value: bool) -> Tuple[Literal["is_public"], bool]:
        return "is_public", value

    @parametrize(value=[i for i in ProviderStatus])
    def case_status(
        self, value: ProviderStatus
    ) -> Tuple[Literal["status"], ProviderStatus]:
        return "status", value

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
        self, len: int
    ) -> Tuple[Literal["projects"], List[ProjectCreate]]:
        if len == 1:
            return "projects", [ProjectCreate(**project_schema_dict())]
        elif len == 2:
            return "projects", [
                ProjectCreate(**project_schema_dict()),
                ProjectCreate(**project_schema_dict()),
            ]
        else:
            return "projects", []

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2])
    def case_regions(
        self, len: int
    ) -> Tuple[Literal["regions"], List[RegionCreateExtended]]:
        if len == 1:
            return "regions", [RegionCreateExtended(**region_schema_dict())]
        elif len == 2:
            return "regions", [
                RegionCreateExtended(**region_schema_dict()),
                RegionCreateExtended(**region_schema_dict()),
            ]
        else:
            return "regions", []

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2])
    def case_identity_providers(
        self, user_group_create_ext_schema: UserGroupCreateExtended, len: int
    ) -> Tuple[Literal["identity_providers"], List[IdentityProviderCreateExtended]]:
        if len == 1:
            return "identity_providers", [
                IdentityProviderCreateExtended(
                    **identity_provider_schema_dict(),
                    relationship=auth_method_dict(),
                    user_groups=[user_group_create_ext_schema],
                )
            ]
        elif len == 2:
            return "identity_providers", [
                IdentityProviderCreateExtended(
                    **identity_provider_schema_dict(),
                    relationship=auth_method_dict(),
                    user_groups=[user_group_create_ext_schema],
                ),
                IdentityProviderCreateExtended(
                    **identity_provider_schema_dict(),
                    relationship=auth_method_dict(),
                    user_groups=[
                        UserGroupCreateExtended(
                            **user_group_schema_dict(),
                            sla=SLACreateExtended(**sla_schema_dict(), project=uuid4()),
                        )
                    ],
                ),
            ]
        else:
            return "identity_providers", []


class CaseInvalidAttr:
    @case(tags=["base_public", "update"])
    @parametrize(attr=["name", "type"])
    def case_attr(self, attr: str) -> Tuple[str, None]:
        return attr, None

    @case(tags=["base_public"])
    def case_type(self) -> Tuple[Literal["type"], str]:
        return "type", random_lower_string()

    def case_status(self) -> Tuple[Literal["status"], str]:
        return "status", random_lower_string()

    def case_email(self) -> Tuple[Literal["support_emails"], List[str]]:
        return "support_emails", [random_lower_string()]

    @case(tags=["create_extended"])
    @parametrize(attr=["name", "uuid"])
    def case_dup_projects(
        self, attr: str
    ) -> Tuple[Literal["projects"], List[ProjectCreate]]:
        project = ProjectCreate(**project_schema_dict())
        project2 = project.copy()
        if attr == "name":
            project2.uuid = uuid4().hex
        else:
            project2.name = random_lower_string()
        return (
            "projects",
            [project, project2],
            f"There are multiple items with identical {attr}",
        )

    @case(tags=["create_extended"])
    def case_dup_regions(self) -> Tuple[Literal["regions"], List[RegionCreateExtended]]:
        region = RegionCreateExtended(**project_schema_dict())
        return (
            "regions",
            [region, region],
            "There are multiple items with identical name",
        )

    @case(tags=["create_extended"])
    def case_dup_idps(
        self, user_group_create_ext_schema: IdentityProviderCreateExtended
    ) -> Tuple[Literal["identity_providers"], List[ProjectCreate]]:
        idp = IdentityProviderCreateExtended(
            **identity_provider_schema_dict(),
            relationship=auth_method_dict(),
            user_groups=[user_group_create_ext_schema],
        )
        return (
            "identity_providers",
            [idp, idp],
            "There are multiple items with identical endpoint",
        )


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


@parametrize_with_cases(
    "key, value", cases=CaseAttr, filter=lambda f: not f.has_tag("create_extended")
)
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


@parametrize_with_cases(
    "key, value",
    cases=CaseInvalidAttr,
    filter=lambda f: not f.has_tag("create_extended"),
)
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
        projects = []
        for idp in values:
            for user_group in idp.user_groups:
                projects.append(user_group.sla.project)
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
    with pytest.raises(ValueError, match=msg):
        ProviderCreateExtended(**d)


# @parametrize_with_cases(
#     "attr, values, msg", cases=CaseInvalidAttr, has_tag=["create_extended"]
# )
# def test_invalid_projects_create_extended(
#     attr: str,
#     values: Union[
#         List[IdentityProviderCreateExtended],
#         List[ProjectCreate],
#         List[RegionCreateExtended],
#     ],
#     msg: str,
# ) -> None:
#     assert issubclass(ProviderCreateExtended, ProviderCreate)
#     d = provider_schema_dict()
#     d[attr] = values
#     with pytest.raises(ValueError, match=msg):
#         ProviderCreateExtended(**d)

# TODO CreateExtended -> IDP projects do not exist or are duplicated
#                     -> Services' quotas and resources' projects do not exist
# TODO Update functions in schemas_extended.py
# TODO Test all read classes
