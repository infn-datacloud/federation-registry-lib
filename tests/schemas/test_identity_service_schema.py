from typing import Any, Literal, Tuple

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from fed_reg.service.enum import IdentityServiceName, ServiceType
from fed_reg.service.models import IdentityService
from fed_reg.service.schemas import (
    IdentityServiceBase,
    IdentityServiceCreate,
    IdentityServiceQuery,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    IdentityServiceUpdate,
    ServiceBase,
)
from tests.create_dict import identity_service_schema_dict
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @parametrize(value=[i for i in IdentityServiceName])
    def case_name(self, value: int) -> Tuple[Literal["name"], int]:
        return "name", value


class CaseInvalidAttr:
    @case(tags=["update"])
    @parametrize(attr=["endpoint", "name"])
    def case_none(self, attr: str) -> Tuple[str, None]:
        return attr, None

    def case_endpoint(self) -> Tuple[Literal["endpoint"], None]:
        return "endpoint", random_lower_string()

    @parametrize(value=[i for i in ServiceType if i != ServiceType.IDENTITY])
    def case_type(self, value: ServiceType) -> Tuple[Literal["type"], ServiceType]:
        return "type", value


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_base(key: str, value: Any) -> None:
    assert issubclass(IdentityServiceBase, ServiceBase)
    d = identity_service_schema_dict()
    if key:
        d[key] = value
    item = IdentityServiceBase(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.type == ServiceType.IDENTITY.value
    assert item.name == d.get("name").value


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_base(key: str, value: Any) -> None:
    d = identity_service_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        IdentityServiceBase(**d)


def test_create() -> None:
    assert issubclass(IdentityServiceCreate, BaseNodeCreate)
    assert issubclass(IdentityServiceCreate, IdentityServiceBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(IdentityServiceUpdate, BaseNodeCreate)
    assert issubclass(IdentityServiceUpdate, IdentityServiceBase)
    d = identity_service_schema_dict()
    if key:
        d[key] = value
    item = IdentityServiceUpdate(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.type == ServiceType.IDENTITY.value
    assert item.name == (d.get("name").value if d.get("name") else None)


def test_query() -> None:
    assert issubclass(IdentityServiceQuery, BaseNodeQuery)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_read_public(
    identity_service_model: IdentityService, key: str, value: str
) -> None:
    assert issubclass(IdentityServiceReadPublic, ServiceBase)
    assert issubclass(IdentityServiceReadPublic, BaseNodeRead)
    assert IdentityServiceReadPublic.__config__.orm_mode

    if key:
        identity_service_model.__setattr__(key, value)
    item = IdentityServiceReadPublic.from_orm(identity_service_model)

    assert item.uid
    assert item.uid == identity_service_model.uid
    assert item.description == identity_service_model.description
    assert item.endpoint == identity_service_model.endpoint


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_read(identity_service_model: IdentityService, key: str, value: Any) -> None:
    assert issubclass(IdentityServiceRead, IdentityServiceBase)
    assert issubclass(IdentityServiceRead, BaseNodeRead)
    assert IdentityServiceRead.__config__.orm_mode

    if key:
        if isinstance(value, IdentityServiceName):
            value = value.value
        identity_service_model.__setattr__(key, value)
    item = IdentityServiceRead.from_orm(identity_service_model)

    assert item.uid
    assert item.uid == identity_service_model.uid
    assert item.description == identity_service_model.description
    assert item.endpoint == identity_service_model.endpoint
    assert item.type == identity_service_model.type
    assert item.name == identity_service_model.name


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_read(
    identity_service_model: IdentityService, key: str, value: str
) -> None:
    identity_service_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        IdentityServiceRead.from_orm(identity_service_model)


# TODO Test read extended classes
