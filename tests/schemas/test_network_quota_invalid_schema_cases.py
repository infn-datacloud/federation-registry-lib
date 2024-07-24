from random import randint
from typing import Literal

from pytest_cases import parametrize

from fed_reg.quota.enum import QuotaType


class CaseInvalidAttr:
    @parametrize(
        attr=(
            "public_ips",
            "networks",
            "ports",
            "security_groups",
            "security_group_rules",
        )
    )
    def case_integer(self, attr: str) -> tuple[str, int]:
        return attr, randint(-100, -2)

    @parametrize(value=(i for i in QuotaType if i != QuotaType.NETWORK))
    def case_type(self, value: QuotaType) -> tuple[Literal["type"], QuotaType]:
        return "type", value
