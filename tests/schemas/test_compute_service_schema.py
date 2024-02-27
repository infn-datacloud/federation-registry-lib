from typing import Any, List, Literal, Tuple, Union
from uuid import uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNodeCreate, BaseNodeQuery
from fed_reg.provider.schemas_extended import (
    ComputeQuotaCreateExtended,
    ComputeServiceCreateExtended,
    FlavorCreateExtended,
    ImageCreateExtended,
)
from fed_reg.service.enum import ComputeServiceName, ServiceType
from fed_reg.service.schemas import (
    ComputeServiceBase,
    ComputeServiceCreate,
    ComputeServiceQuery,
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
    @case(tags=["update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @parametrize(value=[i for i in ComputeServiceName])
    def case_name(self, value: int) -> Tuple[Literal["name"], int]:
        return "name", value

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2, 3])
    def case_quotas(
        self, len: int
    ) -> Tuple[Literal["quotas"], List[ComputeQuotaCreateExtended]]:
        if len == 1:
            return "quotas", [ComputeQuotaCreateExtended(project=uuid4())]
        elif len == 2:
            return "quotas", [
                ComputeQuotaCreateExtended(project=uuid4()),
                ComputeQuotaCreateExtended(project=uuid4()),
            ]
        elif len == 3:
            # Same project, different users scope
            project = uuid4()
            return "quotas", [
                ComputeQuotaCreateExtended(per_user=True, project=project),
                ComputeQuotaCreateExtended(per_user=False, project=project),
            ]
        else:
            return "quotas", []

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2])
    def case_flavors(
        self, len: int
    ) -> Tuple[Literal["flavors"], List[FlavorCreateExtended]]:
        if len == 1:
            return "flavors", [FlavorCreateExtended(**flavor_schema_dict())]
        elif len == 2:
            return "flavors", [
                FlavorCreateExtended(**flavor_schema_dict()),
                FlavorCreateExtended(**flavor_schema_dict()),
            ]
        else:
            return "flavors", []

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2])
    def case_images(
        self, len: int
    ) -> Tuple[Literal["images"], List[ImageCreateExtended]]:
        if len == 1:
            return "images", [ImageCreateExtended(**image_schema_dict())]
        elif len == 2:
            return "images", [
                ImageCreateExtended(**image_schema_dict()),
                ImageCreateExtended(**image_schema_dict()),
            ]
        else:
            return "images", []


class CaseInvalidAttr:
    @case(tags=["update"])
    @parametrize(attr=["endpoint", "name"])
    def case_none(self, attr: str) -> Tuple[str, None]:
        return attr, None

    def case_endpoint(self) -> Tuple[Literal["endpoint"], None]:
        return "endpoint", random_lower_string()

    @parametrize(value=[i for i in ServiceType if i != ServiceType.COMPUTE])
    def case_type(self, value: ServiceType) -> Tuple[Literal["type"], ServiceType]:
        return "type", value

    @case(tags=["create_extended"])
    def case_dup_quotas(
        self,
    ) -> Tuple[Literal["quotas"], List[ComputeQuotaCreateExtended], str]:
        quota = ComputeQuotaCreateExtended(project=uuid4())
        return "quotas", [quota, quota], "Multiple quotas on same project"

    @case(tags=["create_extended"])
    @parametrize(attr=["name", "uuid"])
    @parametrize(res=["flavors", "images"])
    def case_dup_res(
        self, attr: str, res: str
    ) -> Tuple[str, Union[List[FlavorCreateExtended], List[ImageCreateExtended]], str]:
        if res == "flavors":
            item = FlavorCreateExtended(**flavor_schema_dict())
        else:
            item = ImageCreateExtended(**image_schema_dict())
        item2 = item.copy()
        if attr == "name":
            item2.uuid = uuid4().hex
        else:
            item2.name = random_lower_string()
        return (
            res,
            [item, item2],
            f"There are multiple items with identical {attr}",
        )


@parametrize_with_cases(
    "key, value", cases=CaseAttr, filter=lambda f: not f.has_tag("create_extended")
)
def test_base(key: str, value: Any) -> None:
    assert issubclass(ComputeServiceBase, ServiceBase)
    d = compute_service_schema_dict()
    if key:
        d[key] = value
    item = ComputeServiceBase(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.type == ServiceType.COMPUTE.value
    assert item.name == d.get("name").value


@parametrize_with_cases(
    "key, value",
    cases=CaseInvalidAttr,
    filter=lambda f: not f.has_tag("create_extended"),
)
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
    values: Union[
        List[ComputeQuotaCreateExtended],
        List[FlavorCreateExtended],
        List[ImageCreateExtended],
    ],
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
    attr: str, values: List[ComputeQuotaCreateExtended], msg: str
) -> None:
    assert issubclass(ComputeServiceCreateExtended, ComputeServiceCreate)
    d = compute_service_schema_dict()
    d[attr] = values
    with pytest.raises(ValueError, match=msg):
        ComputeServiceCreateExtended(**d)


# TODO Test all read classes
