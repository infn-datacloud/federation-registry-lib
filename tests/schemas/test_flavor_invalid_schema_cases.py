from typing import Literal
from uuid import UUID, uuid4

from pytest_cases import case, parametrize

from tests.utils import random_lower_string


class CaseInvalidAttr:
    @case(tags=["base_public", "base"])
    @parametrize(attr=["name", "uuid"])
    def case_attr(self, attr: str) -> tuple[str, None]:
        return attr, None

    @case(tags=["base"])
    @parametrize(attr=["disk", "ram", "vcpus", "swap", "ephemeral", "gpus"])
    def case_integer(self, attr: str) -> tuple[str, Literal[-1]]:
        return attr, -1

    @case(tags=["base"])
    @parametrize(attr=["gpu_model", "gpu_vendor"])
    def case_gpu_details(self, attr: str) -> tuple[str, str]:
        return attr, random_lower_string()

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2])
    def case_projects(self, len: int) -> tuple[list[UUID], str]:
        if len == 1:
            return [uuid4()], "Public flavors do not have linked projects"
        elif len == 2:
            i = uuid4()
            return [i, i], "There are multiple identical items"
        return [], "Projects are mandatory for private flavors"
