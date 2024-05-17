from typing import Any, Literal
from uuid import uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNodeCreate, BaseNodeQuery, BaseNodeRead
from fed_reg.provider.schemas_extended import (
    ObjectStorageQuotaCreateExtended,
    ObjectStorageServiceCreateExtended,
)
from fed_reg.service.enum import ObjectStorageServiceName, ServiceType
from fed_reg.service.models import ObjectStorageService
from fed_reg.service.schemas import (
    ObjectStorageServiceBase,
    ObjectStorageServiceCreate,
    ObjectStorageServiceQuery,
    ObjectStorageServiceRead,
    ObjectStorageServiceReadPublic,
    ObjectStorageServiceUpdate,
    ServiceBase,
)
from tests.create_dict import object_storage_service_schema_dict
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "base", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["base_public", "base"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @case(tags=["base"])
    @parametrize(value=[i for i in ObjectStorageServiceName])
    def case_name(self, value: int) -> tuple[Literal["name"], int]:
        return "name", value

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2, 3])
    def case_quotas(
        self,
        object_storage_quota_create_ext_schema: ObjectStorageQuotaCreateExtended,
        len: int,
    ) -> list[ObjectStorageQuotaCreateExtended]:
        if len == 1:
            return [object_storage_quota_create_ext_schema]
        elif len == 2:
            return [
                object_storage_quota_create_ext_schema,
                ObjectStorageQuotaCreateExtended(project=uuid4()),
            ]
        elif len == 3:
            # Same project, different users scope
            quota2 = object_storage_quota_create_ext_schema.copy()
            quota2.per_user = not quota2.per_user
            return [object_storage_quota_create_ext_schema, quota2]
        else:
            return []


class CaseInvalidAttr:
    @case(tags=["base", "update"])
    @parametrize(attr=["endpoint", "name"])
    def case_none(self, attr: str) -> tuple[str, None]:
        return attr, None

    @case(tags=["base"])
    def case_endpoint(self) -> tuple[Literal["endpoint"], None]:
        return "endpoint", random_lower_string()

    @case(tags=["base"])
    @parametrize(value=[i for i in ServiceType if i != ServiceType.OBJECT_STORAGE])
    def case_type(self, value: ServiceType) -> tuple[Literal["type"], ServiceType]:
        return "type", value

    @case(tags=["create_extended"])
    def case_dup_quotas(
        self, object_storage_quota_create_ext_schema: ObjectStorageQuotaCreateExtended
    ) -> tuple[list[ObjectStorageQuotaCreateExtended], str]:
        return [
            object_storage_quota_create_ext_schema,
            object_storage_quota_create_ext_schema,
        ], "Multiple quotas on same project"


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base"])
def test_base(key: str, value: Any) -> None:
    assert issubclass(ObjectStorageServiceBase, ServiceBase)
    d = object_storage_service_schema_dict()
    if key:
        d[key] = value
    item = ObjectStorageServiceBase(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.type == ServiceType.OBJECT_STORAGE.value
    assert item.name == d.get("name").value


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base"])
def test_invalid_base(key: str, value: Any) -> None:
    d = object_storage_service_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ObjectStorageServiceBase(**d)


def test_create() -> None:
    assert issubclass(ObjectStorageServiceCreate, BaseNodeCreate)
    assert issubclass(ObjectStorageServiceCreate, ObjectStorageServiceBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(ObjectStorageServiceUpdate, BaseNodeCreate)
    assert issubclass(ObjectStorageServiceUpdate, ObjectStorageServiceBase)
    d = object_storage_service_schema_dict()
    if key:
        d[key] = value
    item = ObjectStorageServiceUpdate(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.type == ServiceType.OBJECT_STORAGE.value
    assert item.name == (d.get("name").value if d.get("name") else None)


def test_query() -> None:
    assert issubclass(ObjectStorageServiceQuery, BaseNodeQuery)


@parametrize_with_cases("quotas", cases=CaseAttr, has_tag=["create_extended"])
def test_create_extended(quotas: list[ObjectStorageQuotaCreateExtended]) -> None:
    assert issubclass(ObjectStorageServiceCreateExtended, ObjectStorageServiceCreate)
    d = object_storage_service_schema_dict()
    d["quotas"] = quotas
    item = ObjectStorageServiceCreateExtended(**d)
    assert item.quotas == quotas


@parametrize_with_cases(
    "quotas, msg", cases=CaseInvalidAttr, has_tag=["create_extended"]
)
def test_invalid_create_extended(
    quotas: list[ObjectStorageQuotaCreateExtended], msg: str
) -> None:
    d = object_storage_service_schema_dict()
    d["quotas"] = quotas
    with pytest.raises(ValueError, match=msg):
        ObjectStorageServiceCreateExtended(**d)


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_read_public(
    object_storage_service_model: ObjectStorageService, key: str, value: str
) -> None:
    assert issubclass(ObjectStorageServiceReadPublic, ServiceBase)
    assert issubclass(ObjectStorageServiceReadPublic, BaseNodeRead)
    assert ObjectStorageServiceReadPublic.__config__.orm_mode

    if key:
        object_storage_service_model.__setattr__(key, value)
    item = ObjectStorageServiceReadPublic.from_orm(object_storage_service_model)

    assert item.uid
    assert item.uid == object_storage_service_model.uid
    assert item.description == object_storage_service_model.description
    assert item.endpoint == object_storage_service_model.endpoint


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base"])
def test_read(
    object_storage_service_model: ObjectStorageService, key: str, value: Any
) -> None:
    assert issubclass(ObjectStorageServiceRead, ObjectStorageServiceBase)
    assert issubclass(ObjectStorageServiceRead, BaseNodeRead)
    assert ObjectStorageServiceRead.__config__.orm_mode

    if key:
        if isinstance(value, ObjectStorageServiceName):
            value = value.value
        object_storage_service_model.__setattr__(key, value)
    item = ObjectStorageServiceRead.from_orm(object_storage_service_model)

    assert item.uid
    assert item.uid == object_storage_service_model.uid
    assert item.description == object_storage_service_model.description
    assert item.endpoint == object_storage_service_model.endpoint
    assert item.type == object_storage_service_model.type
    assert item.name == object_storage_service_model.name


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base"])
def test_invalid_read(
    object_storage_service_model: ObjectStorageService, key: str, value: str
) -> None:
    object_storage_service_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ObjectStorageServiceRead.from_orm(object_storage_service_model)


# TODO Test read extended classes
