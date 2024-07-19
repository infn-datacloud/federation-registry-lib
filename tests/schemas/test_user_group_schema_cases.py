from typing import Literal

from pytest_cases import case

from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base", "base_public", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["update"])
    def case_attr(self) -> tuple[Literal["name"], None]:
        return "name", None

    @case(tags=["base", "base_public"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()
