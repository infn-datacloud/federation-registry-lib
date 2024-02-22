from typing import Literal, Tuple

from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.models import BaseNode
from fed_reg.quota.schemas import QuotaBase
from tests.utils import random_lower_string


class CaseAttr:
    def case_none(self) -> Tuple[None, None]:
        return None, None

    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @parametrize(value=[True, False])
    def case_boolean(self, value: bool) -> Tuple[Literal["per_user"], bool]:
        return "per_user", value


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_base_public(key: str, value: str) -> None:
    assert issubclass(QuotaBase, BaseNode)
    d = {key: value} if key else {}
    item = QuotaBase(**d)
    assert item.description == d.get("description", "")
    assert item.per_user == d.get("per_user", False)
