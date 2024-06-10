from typing import Any, Literal
from uuid import uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from fed_reg.provider.schemas_extended import (
    ComputeQuotaCreateExtended,
    ComputeServiceCreateExtended,
    FlavorCreateExtended,
    ImageCreateExtended,
)
from fed_reg.service.enum import ComputeServiceName, ServiceType
from fed_reg.service.models import ComputeService
from fed_reg.service.schemas import (
    ComputeServiceBase,
    ComputeServiceCreate,
    ComputeServiceQuery,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    ComputeServiceUpdate,
    ServiceBase,
)
from tests.create_dict import (
    compute_service_schema_dict,
    flavor_schema_dict,
    image_schema_dict,
)
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "base", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["base_public", "base"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @case(tags=["base"])
    @parametrize(value=[i for i in ComputeServiceName])
    def case_name(self, value: int) -> tuple[Literal["name"], int]:
        return "name", value

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2, 3])
    def case_quotas(
        self, compute_quota_create_ext_schema: ComputeQuotaCreateExtended, len: int
    ) -> tuple[Literal["quotas"], list[ComputeQuotaCreateExtended]]:
        if len == 1:
            return "quotas", [compute_quota_create_ext_schema]
        elif len == 2:
            return "quotas", [
                compute_quota_create_ext_schema,
                ComputeQuotaCreateExtended(project=uuid4()),
            ]
        elif len == 3:
            # Same project, different users scope
            quota2 = compute_quota_create_ext_schema.copy()
            quota2.per_user = not quota2.per_user
            return "quotas", [compute_quota_create_ext_schema, quota2]
        else:
            return "quotas", []

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2])
    def case_flavors(
        self, flavor_create_ext_schema: FlavorCreateExtended, len: int
    ) -> tuple[Literal["flavors"], list[FlavorCreateExtended]]:
        if len == 1:
            return "flavors", [flavor_create_ext_schema]
        elif len == 2:
            return "flavors", [
                flavor_create_ext_schema,
                FlavorCreateExtended(**flavor_schema_dict()),
            ]
        else:
            return "flavors", []

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2])
    def case_images(
        self, image_create_ext_schema: ImageCreateExtended, len: int
    ) -> tuple[Literal["images"], list[ImageCreateExtended]]:
        if len == 1:
            return "images", [image_create_ext_schema]
        elif len == 2:
            return "images", [
                image_create_ext_schema,
                ImageCreateExtended(**image_schema_dict()),
            ]
        else:
            return "images", []


class CaseInvalidAttr:
    @case(tags=["base", "update"])
    @parametrize(attr=["endpoint", "name"])
    def case_none(self, attr: str) -> tuple[str, None]:
        return attr, None

    @case(tags=["base"])
    def case_endpoint(self) -> tuple[Literal["endpoint"], None]:
        return "endpoint", random_lower_string()

    @case(tags=["base"])
    @parametrize(value=[i for i in ServiceType if i != ServiceType.COMPUTE])
    def case_type(self, value: ServiceType) -> tuple[Literal["type"], ServiceType]:
        return "type", value

    @case(tags=["create_extended"])
    def case_dup_quotas(
        self, compute_quota_create_ext_schema: ComputeQuotaCreateExtended
    ) -> tuple[Literal["quotas"], list[ComputeQuotaCreateExtended], str]:
        return (
            "quotas",
            [compute_quota_create_ext_schema, compute_quota_create_ext_schema],
            "Multiple quotas on same project",
        )

    @case(tags=["create_extended"])
    @parametrize(attr=["name", "uuid"])
    @parametrize(res=["flavors", "images"])
    def case_dup_res(
        self,
        flavor_create_ext_schema: FlavorCreateExtended,
        image_create_ext_schema: ImageCreateExtended,
        attr: str,
        res: str,
    ) -> tuple[str, list[FlavorCreateExtended] | list[ImageCreateExtended], str]:
        item = flavor_create_ext_schema if res == "flavors" else image_create_ext_schema
        item2 = item.copy()
        if attr == "name":
            item2.uuid = uuid4()
        else:
            item2.name = random_lower_string()
        return (
            res,
            [item, item2],
            f"There are multiple items with identical {attr}",
        )


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base"])
def test_base(key: str, value: Any) -> None:
    assert issubclass(ComputeServiceBase, ServiceBase)
    d = compute_service_schema_dict()
    if key:
        d[key] = value
    item = ComputeServiceBase(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.type == ServiceType.COMPUTE.value
    assert item.name == d.get("name").value


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base"])
def test_invalid_base(key: str, value: Any) -> None:
    d = compute_service_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ComputeServiceBase(**d)


def test_create() -> None:
    assert issubclass(ComputeServiceCreate, BaseNodeCreate)
    assert issubclass(ComputeServiceCreate, ComputeServiceBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(ComputeServiceUpdate, BaseNodeCreate)
    assert issubclass(ComputeServiceUpdate, ComputeServiceBase)
    d = compute_service_schema_dict()
    if key:
        d[key] = value
    item = ComputeServiceUpdate(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.type == ServiceType.COMPUTE.value
    assert item.name == (d.get("name").value if d.get("name") else None)


def test_query() -> None:
    assert issubclass(ComputeServiceQuery, BaseNodeQuery)


@parametrize_with_cases("attr, values", cases=CaseAttr, has_tag=["create_extended"])
def test_create_extended(
    attr: str,
    values: list[ComputeQuotaCreateExtended]
    | list[FlavorCreateExtended]
    | list[ImageCreateExtended],
) -> None:
    assert issubclass(ComputeServiceCreateExtended, ComputeServiceCreate)
    d = compute_service_schema_dict()
    d[attr] = values
    item = ComputeServiceCreateExtended(**d)
    assert item.__getattribute__(attr) == values


@parametrize_with_cases(
    "attr, values, msg", cases=CaseInvalidAttr, has_tag=["create_extended"]
)
def test_invalid_create_extended(
    attr: str, values: list[ComputeQuotaCreateExtended], msg: str
) -> None:
    d = compute_service_schema_dict()
    d[attr] = values
    with pytest.raises(ValueError, match=msg):
        ComputeServiceCreateExtended(**d)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_read_public(
    compute_service_model: ComputeService, key: str, value: str
) -> None:
    assert issubclass(ComputeServiceReadPublic, ServiceBase)
    assert issubclass(ComputeServiceReadPublic, BaseNodeRead)
    assert ComputeServiceReadPublic.__config__.orm_mode

    if key:
        compute_service_model.__setattr__(key, value)
    item = ComputeServiceReadPublic.from_orm(compute_service_model)

    assert item.uid
    assert item.uid == compute_service_model.uid
    assert item.description == compute_service_model.description
    assert item.endpoint == compute_service_model.endpoint


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base"])
def test_read(compute_service_model: ComputeService, key: str, value: Any) -> None:
    assert issubclass(ComputeServiceRead, ComputeServiceBase)
    assert issubclass(ComputeServiceRead, BaseNodeRead)
    assert ComputeServiceRead.__config__.orm_mode

    if key:
        if isinstance(value, ComputeServiceName):
            value = value.value
        compute_service_model.__setattr__(key, value)
    item = ComputeServiceRead.from_orm(compute_service_model)

    assert item.uid
    assert item.uid == compute_service_model.uid
    assert item.description == compute_service_model.description
    assert item.endpoint == compute_service_model.endpoint
    assert item.type == compute_service_model.type
    assert item.name == compute_service_model.name


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base"])
def test_invalid_read(
    compute_service_model: ComputeService, key: str, value: str
) -> None:
    compute_service_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ComputeServiceRead.from_orm(compute_service_model)


# TODO Test read extended classes
