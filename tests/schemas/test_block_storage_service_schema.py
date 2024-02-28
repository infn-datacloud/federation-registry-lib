from typing import Any, List, Literal, Tuple
from uuid import uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNodeCreate, BaseNodeQuery
from fed_reg.provider.schemas_extended import (
    BlockStorageQuotaCreateExtended,
    BlockStorageServiceCreateExtended,
)
from fed_reg.service.enum import BlockStorageServiceName, ServiceType
from fed_reg.service.schemas import (
    BlockStorageServiceBase,
    BlockStorageServiceCreate,
    BlockStorageServiceQuery,
    BlockStorageServiceUpdate,
    ServiceBase,
)
from tests.create_dict import block_storage_service_schema_dict
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @parametrize(value=[i for i in BlockStorageServiceName])
    def case_name(self, value: int) -> Tuple[Literal["name"], int]:
        return "name", value

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2, 3])
    def case_quotas(
        self,
        block_storage_quota_create_ext_schema: BlockStorageQuotaCreateExtended,
        len: int,
    ) -> List[BlockStorageQuotaCreateExtended]:
        if len == 1:
            return [block_storage_quota_create_ext_schema]
        elif len == 2:
            return [
                block_storage_quota_create_ext_schema,
                BlockStorageQuotaCreateExtended(project=uuid4()),
            ]
        elif len == 3:
            # Same project, different users scope
            quota2 = block_storage_quota_create_ext_schema.copy()
            quota2.per_user = not quota2.per_user
            return [block_storage_quota_create_ext_schema, quota2]
        else:
            return []


class CaseInvalidAttr:
    @case(tags=["update"])
    @parametrize(attr=["endpoint", "name"])
    def case_none(self, attr: str) -> Tuple[str, None]:
        return attr, None

    def case_endpoint(self) -> Tuple[Literal["endpoint"], None]:
        return "endpoint", random_lower_string()

    @parametrize(value=[i for i in ServiceType if i != ServiceType.BLOCK_STORAGE])
    def case_type(self, value: ServiceType) -> Tuple[Literal["type"], ServiceType]:
        return "type", value

    @case(tags=["create_extended"])
    def case_dup_quotas(
        self, block_storage_quota_create_ext_schema: BlockStorageQuotaCreateExtended
    ) -> Tuple[List[BlockStorageQuotaCreateExtended], str]:
        return [
            block_storage_quota_create_ext_schema,
            block_storage_quota_create_ext_schema,
        ], "Multiple quotas on same project"


@parametrize_with_cases(
    "key, value", cases=CaseAttr, filter=lambda f: not f.has_tag("create_extended")
)
def test_base(key: str, value: Any) -> None:
    assert issubclass(BlockStorageServiceBase, ServiceBase)
    d = block_storage_service_schema_dict()
    if key:
        d[key] = value
    item = BlockStorageServiceBase(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.type == ServiceType.BLOCK_STORAGE.value
    assert item.name == d.get("name").value


@parametrize_with_cases(
    "key, value",
    cases=CaseInvalidAttr,
    filter=lambda f: not f.has_tag("create_extended"),
)
def test_invalid_base(key: str, value: Any) -> None:
    d = block_storage_service_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        BlockStorageServiceBase(**d)


def test_create() -> None:
    assert issubclass(BlockStorageServiceCreate, BaseNodeCreate)
    assert issubclass(BlockStorageServiceCreate, BlockStorageServiceBase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(BlockStorageServiceUpdate, BaseNodeCreate)
    assert issubclass(BlockStorageServiceUpdate, BlockStorageServiceBase)
    d = block_storage_service_schema_dict()
    if key:
        d[key] = value
    item = BlockStorageServiceUpdate(**d)
    assert item.endpoint == d.get("endpoint")
    assert item.type == ServiceType.BLOCK_STORAGE.value
    assert item.name == (d.get("name").value if d.get("name") else None)


def test_query() -> None:
    assert issubclass(BlockStorageServiceQuery, BaseNodeQuery)


@parametrize_with_cases("quotas", cases=CaseAttr, has_tag=["create_extended"])
def test_create_extended(quotas: List[BlockStorageQuotaCreateExtended]) -> None:
    assert issubclass(BlockStorageServiceCreateExtended, BlockStorageServiceCreate)
    d = block_storage_service_schema_dict()
    d["quotas"] = quotas
    item = BlockStorageServiceCreateExtended(**d)
    assert item.quotas == quotas


@parametrize_with_cases(
    "quotas, msg", cases=CaseInvalidAttr, has_tag=["create_extended"]
)
def test_invalid_create_extended(
    quotas: List[BlockStorageQuotaCreateExtended], msg: str
) -> None:
    d = block_storage_service_schema_dict()
    d["quotas"] = quotas
    with pytest.raises(ValueError, match=msg):
        BlockStorageServiceCreateExtended(**d)


# TODO Test all read classes
