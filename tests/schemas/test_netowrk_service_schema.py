from typing import Any, Literal, Tuple

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNodeCreate, BaseNodeQuery
from fed_reg.service.enum import NetworkServiceName, ServiceType
from fed_reg.service.schemas import (
    NetworkServiceBase,
    NetworkServiceCreate,
    NetworkServiceQuery,
    NetworkServiceUpdate,
    ServiceBase,
)
from tests.create_dict import network_service_schema_dict
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @parametrize(value=[i for i in NetworkServiceName])
    def case_name(self, value: int) -> Tuple[Literal["name"], int]:
        return "name", value


class CaseInvalidAttr:
    @case(tags=["update"])
    @parametrize(attr=["endpoint", "name"])
    def case_none(self, attr: str) -> Tuple[str, None]:
        return attr, None

    def case_endpoint(self) -> Tuple[Literal["endpoint"], None]:
        return "endpoint", random_lower_string()

    @parametrize(value=[i for i in ServiceType if i != ServiceType.NETWORK])
    def case_type(self, value: ServiceType) -> Tuple[Literal["type"], ServiceType]:
        return "type", value


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_base(key: str, value: Any) -> None:
    assert issubclass(NetworkServiceBase, ServiceBase)
    d = network_service_schema_dict()
    if key:
        d[key] = value
    item = NetworkServiceBase(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.type == ServiceType.NETWORK.value
    assert item.name == d.get("name").value


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
def test_invalid_base(key: str, value: Any) -> None:
    d = network_service_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        NetworkServiceBase(**d)


def test_create() -> None:
    assert issubclass(NetworkServiceCreate, BaseNodeCreate)
    assert issubclass(NetworkServiceCreate, NetworkServiceBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(NetworkServiceUpdate, BaseNodeCreate)
    assert issubclass(NetworkServiceUpdate, NetworkServiceBase)
    d = network_service_schema_dict()
    if key:
        d[key] = value
    item = NetworkServiceUpdate(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.type == ServiceType.NETWORK.value
    assert item.name == (d.get("name").value if d.get("name") else None)


def test_query() -> None:
    assert issubclass(NetworkServiceQuery, BaseNodeQuery)


# TODO Test all read classes
