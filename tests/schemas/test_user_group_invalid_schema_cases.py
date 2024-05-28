from typing import Literal


class CaseInvalidAttr:
    def case_attr(self) -> tuple[Literal["name"], None]:
        return "name", None
