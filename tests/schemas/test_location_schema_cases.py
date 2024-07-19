from typing import Literal

from pytest_cases import case, parametrize

from tests.utils import (
    random_country,
    random_latitude,
    random_longitude,
    random_lower_string,
)


class CaseAttr:
    @case(tags=["base", "base_public", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["update"])
    @parametrize(attr=["site", "country"])
    def case_attr(self, attr: str) -> tuple[str, None]:
        return attr, None

    @case(tags=["base", "base_public"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @case(tags=["base"])
    def case_latitude(self) -> tuple[Literal["latitude"], float]:
        return "latitude", random_latitude()

    @case(tags=["base"])
    def case_longitude(self) -> tuple[Literal["longitude"], float]:
        return "longitude", random_longitude()

    @case(tags=["base"])
    def case_country(self) -> tuple[Literal["country"], str]:
        return "country", random_country()

    @case(tags=["base"])
    def case_site(self) -> tuple[Literal["site"], str]:
        return "site", random_lower_string()
