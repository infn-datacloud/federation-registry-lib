from typing import Any

import pytest
from pytest_cases import parametrize_with_cases

from fed_reg.provider.schemas_extended import (
    ObjectStorageQuotaCreateExtended,
    ObjectStorageServiceCreateExtended,
)
from fed_reg.service.models import ObjectStorageService
from fed_reg.service.schemas import ObjectStorageServiceBase, ObjectStorageServiceRead
from tests.create_dict import object_storage_service_schema_dict


@parametrize_with_cases("key, value", has_tag="base")
def test_invalid_base(key: str, value: Any) -> None:
    d = object_storage_service_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        ObjectStorageServiceBase(**d)


@parametrize_with_cases("key, value", has_tag="base")
def test_invalid_read(
    object_storage_service_model: ObjectStorageService, key: str, value: str
) -> None:
    object_storage_service_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        ObjectStorageServiceRead.from_orm(object_storage_service_model)


@parametrize_with_cases("quotas, msg", has_tag="create_extended")
def test_invalid_create_extended(
    quotas: list[ObjectStorageQuotaCreateExtended], msg: str
) -> None:
    d = object_storage_service_schema_dict()
    d["quotas"] = quotas
    with pytest.raises(ValueError, match=msg):
        ObjectStorageServiceCreateExtended(**d)


# TODO Test read extended classes
