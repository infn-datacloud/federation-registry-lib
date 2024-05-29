from typing import Literal

from pytest_cases import case, parametrize

from fed_reg.service.enum import ServiceType
from tests.utils import random_lower_string


class CaseInvalidAttr:
    @case(tags=["update"])
    @parametrize(attr=("endpoint", "name"))
    def case_none(self, attr: str) -> tuple[str, None]:
        return attr, None

    def case_endpoint(self) -> tuple[Literal["endpoint"], None]:
        return "endpoint", random_lower_string()

    @parametrize(value=(i for i in ServiceType if i != ServiceType.IDENTITY))
    def case_type(self, value: ServiceType) -> tuple[Literal["type"], ServiceType]:
        return "type", value
