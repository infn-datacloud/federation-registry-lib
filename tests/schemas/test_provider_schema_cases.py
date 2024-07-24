from typing import Literal

from pydantic import EmailStr
from pytest_cases import case, parametrize

from fed_reg.provider.enum import ProviderStatus, ProviderType
from tests.utils import random_email, random_lower_string


class CaseAttr:
    @case(tags=["base_public", "base", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["update"])
    @parametrize(attr=["name", "type"])
    def case_attr(self, attr: str) -> tuple[str, None]:
        return attr, None

    @case(tags=["base_public", "base"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @case(tags=["base_public", "base"])
    @parametrize(value=(i for i in ProviderType))
    def case_provider_type(
        self, value: ProviderType
    ) -> tuple[Literal["type"], ProviderType]:
        return "type", value

    @case(tags=["base"])
    @parametrize(value=(True, False))
    def case_is_public(self, value: bool) -> tuple[Literal["is_public"], bool]:
        return "is_public", value

    @case(tags=["base"])
    @parametrize(value=(i for i in ProviderStatus))
    def case_provider_status(
        self, value: ProviderStatus
    ) -> tuple[Literal["status"], ProviderStatus]:
        return "status", value

    @case(tags=["base"])
    @parametrize(len=(0, 1, 2))
    def case_email_list(
        self, len: int
    ) -> tuple[Literal["support_emails"], list[EmailStr] | None]:
        return "support_emails", [random_email() for _ in range(len)]
