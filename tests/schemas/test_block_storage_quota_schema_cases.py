from random import randint
from typing import Literal

from pytest_cases import case, parametrize

from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @parametrize(value=(-1, randint(0, 100)))
    @parametrize(attr=("gigabytes", "per_volume_gigabytes", "volumes"))
    def case_integer(self, attr: str, value: int) -> tuple[str, int]:
        return attr, value
