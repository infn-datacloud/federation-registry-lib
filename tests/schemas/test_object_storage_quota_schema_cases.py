from typing import Literal

from pytest_cases import case

from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()

    # TODO: set correct attributes
    # @parametrize(value=[-1, randint(0, 100)])
    # @parametrize(attr=["gigabytes", "per_volume_gigabytes", "volumes"])
    # def case_integer(self, attr: str, value: int) -> tuple[str, int]:
    #     return attr, value
