from typing import Literal

from pytest_cases import parametrize

from fed_reg.quota.enum import QuotaType


class CaseInvalidAttr:
    @parametrize(attr=("cores", "instances", "ram"))
    def case_integer(self, attr: str) -> tuple[str, Literal[-1]]:
        return attr, -1

    @parametrize(value=(i for i in QuotaType if i != QuotaType.COMPUTE))
    def case_type(self, value: QuotaType) -> tuple[Literal["type"], QuotaType]:
        return "type", value
