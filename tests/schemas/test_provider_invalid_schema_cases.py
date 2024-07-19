from typing import Literal

from pytest_cases import case, parametrize

from tests.utils import random_lower_string


class CaseInvalidAttr:
    @case(tags=["base_public", "base", "update"])
    @parametrize(attr=("name", "type"))
    def case_attr(self, attr: str) -> tuple[str, None]:
        return attr, None

    @case(tags=["base_public", "base"])
    def case_provider_type(self) -> tuple[Literal["type"], str]:
        return "type", random_lower_string()

    @case(tags=["base"])
    def case_provider_status(self) -> tuple[Literal["status"], str]:
        return "status", random_lower_string()

    @case(tags=["base"])
    def case_email(self) -> tuple[Literal["support_emails"], list[str]]:
        return "support_emails", [random_lower_string()]
