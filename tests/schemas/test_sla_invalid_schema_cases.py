from typing import Literal

from pytest_cases import case, parametrize


class CaseInvalidAttr:
    @case(tags=["base_public"])
    def case_attr(self) -> tuple[Literal["doc_uuid"], None]:
        return "doc_uuid", None

    @parametrize(attr=["start_date", "end_date"])
    def case_nullable_dates(self, attr: str) -> tuple[str, None]:
        return attr, None

    def case_reversed_dates(self) -> tuple[Literal["reversed_dates"], None]:
        return "reversed_dates", None
