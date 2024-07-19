from typing import Literal

from pytest_cases import case, parametrize

from tests.utils import random_lower_string


class CaseInvalidAttr:
    @case(tags=["base_public"])
    @parametrize(attr=["site", "country"])
    def case_attr(self, attr: str) -> tuple[str, None]:
        return attr, None

    @case(tags=["base_public"])
    def case_country(self) -> tuple[Literal["country"], str]:
        return "country", random_lower_string()

    @parametrize(value=[-91.0, 91.0])
    def case_latitude(self, value: float) -> tuple[Literal["latitude"], float]:
        return "latitude", value

    @parametrize(value=[-181.0, 181.0])
    def case_longitude(self, value: float) -> tuple[Literal["longitude"], float]:
        return "longitude", value
