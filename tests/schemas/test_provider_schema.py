from typing import Any, List, Literal, Optional, Tuple

import pytest
from pydantic import EmailStr
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery
from fed_reg.provider.enum import ProviderStatus, ProviderType
from fed_reg.provider.schemas import (
    ProviderBase,
    ProviderBasePublic,
    ProviderCreate,
    ProviderQuery,
    ProviderUpdate,
)
from tests.create_dict import provider_schema_dict
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


@parametrize_with_cases("key, value", cases=CaseAttr)
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


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
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


# TODO Test all read classes
