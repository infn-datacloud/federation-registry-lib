from typing import Literal

from pytest_cases import case, parametrize

from fed_reg.service.enum import IdentityServiceName
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base", "base_public", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["update"])
    @parametrize(attr=("endpoint", "name"))
    def case_attr_is_none(self, attr: str) -> tuple[str, None]:
        return attr, None

    @case(tags=["base", "base", "base_public"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @case(tags=["base"])
    @parametrize(value=(i for i in IdentityServiceName))
    def case_name(self, value: int) -> tuple[Literal["name"], int]:
        return "name", value
