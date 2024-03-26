from typing import Any, Literal, Union
from uuid import uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from fed_reg.provider.schemas_extended import (
    NetworkCreateExtended,
    NetworkQuotaCreateExtended,
    NetworkServiceCreateExtended,
)
from fed_reg.service.enum import NetworkServiceName, ServiceType
from fed_reg.service.models import NetworkService
from fed_reg.service.schemas import (
    NetworkServiceBase,
    NetworkServiceCreate,
    NetworkServiceQuery,
    NetworkServiceRead,
    NetworkServiceReadPublic,
    NetworkServiceUpdate,
    ServiceBase,
)
from tests.create_dict import network_schema_dict, network_service_schema_dict
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "base", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["base_public", "base"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @case(tags=["base"])
    @parametrize(value=[i for i in NetworkServiceName])
    def case_name(self, value: int) -> tuple[Literal["name"], int]:
        return "name", value

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2, 3])
    def case_quotas(
        self, network_quota_create_ext_schema: NetworkQuotaCreateExtended, len: int
    ) -> tuple[Literal["quotas"], list[NetworkQuotaCreateExtended]]:
        if len == 1:
            return "quotas", [network_quota_create_ext_schema]
        elif len == 2:
            return "quotas", [
                network_quota_create_ext_schema,
                NetworkQuotaCreateExtended(project=uuid4()),
            ]
        elif len == 3:
            # Same project, different users scope
            quota2 = network_quota_create_ext_schema.copy()
            quota2.per_user = not quota2.per_user
            return "quotas", [network_quota_create_ext_schema, quota2]
        else:
            return "quotas", []

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2])
    def case_networks(
        self, network_create_ext_schema: NetworkCreateExtended, len: int
    ) -> tuple[Literal["networks"], list[NetworkCreateExtended]]:
        if len == 1:
            return "networks", [network_create_ext_schema]
        elif len == 2:
            return "networks", [
                network_create_ext_schema,
                NetworkCreateExtended(**network_schema_dict()),
            ]
        else:
            return "networks", []


class CaseInvalidAttr:
    @case(tags=["base", "update"])
    @parametrize(attr=["endpoint", "name"])
    def case_none(self, attr: str) -> tuple[str, None]:
        return attr, None

    @case(tags=["base"])
    def case_endpoint(self) -> tuple[Literal["endpoint"], None]:
        return "endpoint", random_lower_string()

    @case(tags=["base"])
    @parametrize(value=[i for i in ServiceType if i != ServiceType.NETWORK])
    def case_type(self, value: ServiceType) -> tuple[Literal["type"], ServiceType]:
        return "type", value

    @case(tags=["create_extended"])
    def case_dup_quotas(
        self, network_quota_create_ext_schema: NetworkQuotaCreateExtended
    ) -> tuple[Literal["quotas"], list[NetworkQuotaCreateExtended], str]:
        return (
            "quotas",
            [network_quota_create_ext_schema, network_quota_create_ext_schema],
            "Multiple quotas on same project",
        )

    @case(tags=["create_extended"])
    def case_dup_networks(
        self, network_create_ext_schema: NetworkCreateExtended
    ) -> tuple[Literal["networks"], list[NetworkCreateExtended], str]:
        return (
            "networks",
            [network_create_ext_schema, network_create_ext_schema],
            "There are multiple items with identical uuid",
        )


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base"])
def test_base(key: str, value: Any) -> None:
    assert issubclass(NetworkServiceBase, ServiceBase)
    d = network_service_schema_dict()
    if key:
        d[key] = value
    item = NetworkServiceBase(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.type == ServiceType.NETWORK.value
    assert item.name == d.get("name").value


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base"])
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
    values: Union[list[NetworkQuotaCreateExtended], list[NetworkCreateExtended]],
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
    attr: str, values: list[NetworkQuotaCreateExtended], msg: str
) -> None:
    d = network_service_schema_dict()
    d[attr] = values
    with pytest.raises(ValueError, match=msg):
        NetworkServiceCreateExtended(**d)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_read_public(
    network_service_model: NetworkService, key: str, value: str
) -> None:
    assert issubclass(NetworkServiceReadPublic, ServiceBase)
    assert issubclass(NetworkServiceReadPublic, BaseNodeRead)
    assert NetworkServiceReadPublic.__config__.orm_mode

    if key:
        network_service_model.__setattr__(key, value)
    item = NetworkServiceReadPublic.from_orm(network_service_model)

    assert item.uid
    assert item.uid == network_service_model.uid
    assert item.description == network_service_model.description
    assert item.endpoint == network_service_model.endpoint


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base"])
def test_read(network_service_model: NetworkService, key: str, value: Any) -> None:
    assert issubclass(NetworkServiceRead, NetworkServiceBase)
    assert issubclass(NetworkServiceRead, BaseNodeRead)
    assert NetworkServiceRead.__config__.orm_mode

    if key:
        if isinstance(value, NetworkServiceName):
            value = value.value
        network_service_model.__setattr__(key, value)
    item = NetworkServiceRead.from_orm(network_service_model)

    assert item.uid
    assert item.uid == network_service_model.uid
    assert item.description == network_service_model.description
    assert item.endpoint == network_service_model.endpoint
    assert item.type == network_service_model.type
    assert item.name == network_service_model.name


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base"])
def test_invalid_read(
    network_service_model: NetworkService, key: str, value: str
) -> None:
    network_service_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        NetworkServiceRead.from_orm(network_service_model)


# TODO Test read extended classes
