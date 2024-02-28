from typing import Any, List, Literal, Tuple, Union
from uuid import uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNodeCreate, BaseNodeQuery
from fed_reg.provider.schemas_extended import (
    NetworkCreateExtended,
    NetworkQuotaCreateExtended,
    NetworkServiceCreateExtended,
)
from fed_reg.service.enum import NetworkServiceName, ServiceType
from fed_reg.service.schemas import (
    NetworkServiceBase,
    NetworkServiceCreate,
    NetworkServiceQuery,
    NetworkServiceUpdate,
    ServiceBase,
)
from tests.create_dict import network_schema_dict, network_service_schema_dict
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

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2, 3])
    def case_quotas(
        self, len: int
    ) -> Tuple[Literal["quotas"], List[NetworkQuotaCreateExtended]]:
        if len == 1:
            return "quotas", [NetworkQuotaCreateExtended(project=uuid4())]
        elif len == 2:
            return "quotas", [
                NetworkQuotaCreateExtended(project=uuid4()),
                NetworkQuotaCreateExtended(project=uuid4()),
            ]
        elif len == 3:
            # Same project, different users scope
            project = uuid4()
            return "quotas", [
                NetworkQuotaCreateExtended(per_user=True, project=project),
                NetworkQuotaCreateExtended(per_user=False, project=project),
            ]
        else:
            return "quotas", []

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2])
    def case_networks(
        self, len: int
    ) -> Tuple[Literal["networks"], List[NetworkCreateExtended]]:
        if len == 1:
            return "networks", [NetworkCreateExtended(**network_schema_dict())]
        elif len == 2:
            return "networks", [
                NetworkCreateExtended(**network_schema_dict()),
                NetworkCreateExtended(**network_schema_dict()),
            ]
        else:
            return "networks", []


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

    @case(tags=["create_extended"])
    def case_dup_quotas(
        self,
    ) -> Tuple[Literal["quotas"], List[NetworkQuotaCreateExtended], str]:
        quota = NetworkQuotaCreateExtended(project=uuid4())
        return "quotas", [quota, quota], "Multiple quotas on same project"

    @case(tags=["create_extended"])
    def case_dup_networks(
        self,
    ) -> Tuple[Literal["networks"], List[NetworkCreateExtended], str]:
        network = NetworkCreateExtended(**network_schema_dict())
        return (
            "networks",
            [network, network],
            "There are multiple items with identical uuid",
        )


@parametrize_with_cases(
    "key, value", cases=CaseAttr, filter=lambda f: not f.has_tag("create_extended")
)
def test_base(key: str, value: Any) -> None:
    assert issubclass(NetworkServiceBase, ServiceBase)
    d = network_service_schema_dict()
    if key:
        d[key] = value
    item = NetworkServiceBase(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.type == ServiceType.NETWORK.value
    assert item.name == d.get("name").value


@parametrize_with_cases(
    "key, value",
    cases=CaseInvalidAttr,
    filter=lambda f: not f.has_tag("create_extended"),
)
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


@parametrize_with_cases("attr, values", cases=CaseAttr, has_tag=["create_extended"])
def test_create_extended(
    attr: str,
    values: Union[List[NetworkQuotaCreateExtended], List[NetworkCreateExtended]],
) -> None:
    assert issubclass(NetworkServiceCreateExtended, NetworkServiceCreate)
    d = network_service_schema_dict()
    d[attr] = values
    item = NetworkServiceCreateExtended(**d)
    assert item.__getattribute__(attr) == values


@parametrize_with_cases(
    "attr, values, msg", cases=CaseInvalidAttr, has_tag=["create_extended"]
)
def test_invalid_create_extended(
    attr: str, values: List[NetworkQuotaCreateExtended], msg: str
) -> None:
    d = network_service_schema_dict()
    d[attr] = values
    with pytest.raises(ValueError, match=msg):
        NetworkServiceCreateExtended(**d)


# TODO Test all read classes
