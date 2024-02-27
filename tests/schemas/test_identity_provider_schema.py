from typing import Any, List, Literal, Optional, Tuple
from uuid import uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.auth_method.schemas import AuthMethodCreate
from fed_reg.identity_provider.schemas import (
    IdentityProviderBase,
    IdentityProviderBasePublic,
    IdentityProviderCreate,
    IdentityProviderQuery,
    IdentityProviderUpdate,
)
from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery
from fed_reg.provider.schemas_extended import (
    IdentityProviderCreateExtended,
    SLACreateExtended,
    UserGroupCreateExtended,
)
from tests.create_dict import (
    auth_method_dict,
    identity_provider_schema_dict,
    sla_schema_dict,
    user_group_schema_dict,
)
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()

    def case_group_claim(self) -> Tuple[Literal["group_claim"], str]:
        return "group_claim", random_lower_string()

    @case(tags=["create_extended"])
    @parametrize(len=[1, 2])
    def case_user_groups(
        self, user_group_create_ext_schema: UserGroupCreateExtended, len: int
    ) -> List[UserGroupCreateExtended]:
        if len == 1:
            return [user_group_create_ext_schema]
        else:
            return [
                user_group_create_ext_schema,
                UserGroupCreateExtended(
                    **user_group_schema_dict(),
                    sla=SLACreateExtended(**sla_schema_dict(), project=uuid4()),
                ),
            ]


class CaseInvalidAttr:
    @case(tags=["base_public", "base", "update"])
    def case_endpoint(self) -> Tuple[Literal["endpoint"], None]:
        return "endpoint", None

    @case(tags=["base", "update"])
    def case_group_claim(self) -> Tuple[Literal["group_claim"], None]:
        return "group_claim", None

    @case(tags=["create_extended"])
    def case_missing_relationship(self) -> Tuple[Literal["relationship"], None, None]:
        return "relationship", None, None

    @case(tags=["create_extended"])
    @parametrize(len=[0, 2])
    def case_user_groups(
        self, user_group_create_ext_schema: UserGroupCreateExtended, len: int
    ) -> Tuple[Literal["user_groups"], List[UserGroupCreateExtended], str]:
        if len == 0:
            return (
                "user_groups",
                [],
                "Identity provider's user group list can't be empty",
            )
        else:
            return (
                "user_groups",
                [
                    user_group_create_ext_schema,
                    user_group_create_ext_schema,
                ],
                "There are multiple items with identical name",
            )


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_base_public(key: str, value: str) -> None:
    assert issubclass(IdentityProviderBasePublic, BaseNode)
    d = identity_provider_schema_dict()
    if key:
        d[key] = value
    item = IdentityProviderBasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.endpoint == d.get("endpoint")


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_base_public(key: str, value: None) -> None:
    d = identity_provider_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        IdentityProviderBasePublic(**d)


@parametrize_with_cases(
    "key, value", cases=CaseAttr, filter=lambda f: not f.has_tag("create_extended")
)
def test_base(key: str, value: Any) -> None:
    assert issubclass(IdentityProviderBase, IdentityProviderBasePublic)
    d = identity_provider_schema_dict()
    if key:
        d[key] = value
    item = IdentityProviderBase(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.group_claim == d.get("group_claim")


@parametrize_with_cases(
    "key, value",
    cases=CaseInvalidAttr,
    filter=lambda f: not f.has_tag("create_extended"),
)
def test_invalid_base(key: str, value: Any) -> None:
    d = identity_provider_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        IdentityProviderBase(**d)


def test_create() -> None:
    assert issubclass(IdentityProviderCreate, BaseNodeCreate)
    assert issubclass(IdentityProviderCreate, IdentityProviderBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(IdentityProviderUpdate, BaseNodeCreate)
    assert issubclass(IdentityProviderUpdate, IdentityProviderBase)
    d = identity_provider_schema_dict()
    if key:
        d[key] = value
    item = IdentityProviderUpdate(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.group_claim == d.get("group_claim")


def test_query() -> None:
    assert issubclass(IdentityProviderQuery, BaseNodeQuery)


@parametrize_with_cases("user_groups", cases=CaseAttr, has_tag="create_extended")
def test_create_extended(user_groups: List[UserGroupCreateExtended]) -> None:
    assert issubclass(IdentityProviderCreateExtended, IdentityProviderCreate)
    d = identity_provider_schema_dict()
    d["relationship"] = AuthMethodCreate(**auth_method_dict())
    d["user_groups"] = user_groups
    item = IdentityProviderCreateExtended(**d)
    assert item.relationship == d["relationship"]
    assert item.user_groups == d["user_groups"]


@parametrize_with_cases(
    "attr, value, msg", cases=CaseInvalidAttr, has_tag=["create_extended"]
)
def test_invalid_create_extended(
    user_group_create_ext_schema: UserGroupCreateExtended,
    attr: str,
    value: UserGroupCreateExtended,
    msg: Optional[str],
) -> None:
    assert issubclass(IdentityProviderCreateExtended, IdentityProviderCreate)
    d = identity_provider_schema_dict()
    d["relationship"] = (
        value if attr == "relationship" else AuthMethodCreate(**auth_method_dict())
    )
    d["user_groups"] = value if attr == "user_groups" else user_group_create_ext_schema
    with pytest.raises(ValueError, match=msg):
        IdentityProviderCreateExtended(**d)


# TODO Test all read classes
