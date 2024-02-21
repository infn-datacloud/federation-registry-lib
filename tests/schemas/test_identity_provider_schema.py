from typing import Any, Literal, Tuple

import pytest
from pytest_cases import case, parametrize_with_cases

from fed_reg.identity_provider.schemas import (
    IdentityProviderBase,
    IdentityProviderBasePublic,
    IdentityProviderCreate,
    IdentityProviderQuery,
    IdentityProviderUpdate,
)
from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery
from tests.create_dict import identity_provider_schema_dict
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


class CaseInvalidAttr:
    @case(tags=["base_public", "base", "update"])
    def case_endpoint(self) -> Tuple[Literal["endpoint"], None]:
        return "endpoint", None

    @case(tags=["base", "update"])
    def case_group_claim(self) -> Tuple[Literal["group_claim"], None]:
        return "group_claim", None


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


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_base(key: str, value: Any) -> None:
    assert issubclass(IdentityProviderBase, IdentityProviderBasePublic)
    d = identity_provider_schema_dict()
    if key:
        d[key] = value
    item = IdentityProviderBase(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.group_claim == d.get("group_claim")


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
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


# TODO Test all read classes
