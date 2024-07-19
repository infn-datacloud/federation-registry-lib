from typing import Literal, Optional
from uuid import UUID, uuid4

from pytest_cases import case, parametrize


class CaseInvalidAttr:
    @case(tags=["base_public", "base"])
    @parametrize(attr=["name", "uuid"])
    def case_attr(self, attr: str) -> tuple[str, None]:
        return attr, None

    @case(tags=["base"])
    @parametrize(attr=["mtu"])
    def case_integer(self, attr: str) -> tuple[str, Literal[-1]]:
        return attr, -1

    @case(tags=["create_extended"])
    @parametrize(with_project=[True, False])
    def case_project(self, with_project: bool) -> tuple[Optional[UUID], str]:
        if with_project:
            return uuid4(), "Shared networks do not have a linked project"
        else:
            return None, "Projects is mandatory for private networks"
