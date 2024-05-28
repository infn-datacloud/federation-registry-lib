from pytest_cases import parametrize


class CaseInvalidAttr:
    @parametrize(attr=["name", "uuid"])
    def case_attr(self, attr: str) -> tuple[str, None]:
        return attr, None
