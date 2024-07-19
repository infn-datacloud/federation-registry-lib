from typing import Literal

from pytest_cases import case, parametrize

from fed_reg.provider.schemas_extended import ObjectStoreQuotaCreateExtended
from fed_reg.service.enum import ServiceType
from tests.utils import random_lower_string


class CaseInvalidAttr:
    @case(tags=["base"])
    @parametrize(attr=("endpoint", "name"))
    def case_none(self, attr: str) -> tuple[str, None]:
        return attr, None

    @case(tags=["base"])
    def case_endpoint(self) -> tuple[Literal["endpoint"], None]:
        return "endpoint", random_lower_string()

    @case(tags=["base"])
    @parametrize(value=(i for i in ServiceType if i != ServiceType.OBJECT_STORE))
    def case_type(self, value: ServiceType) -> tuple[Literal["type"], ServiceType]:
        return "type", value

    @case(tags=["create_extended"])
    def case_dup_quotas(
        self, object_store_quota_create_ext_schema: ObjectStoreQuotaCreateExtended
    ) -> tuple[list[ObjectStoreQuotaCreateExtended], str]:
        return [
            object_store_quota_create_ext_schema,
            object_store_quota_create_ext_schema,
        ], "Multiple quotas on same project"
