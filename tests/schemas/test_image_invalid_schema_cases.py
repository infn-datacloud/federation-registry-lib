from uuid import UUID, uuid4

from pytest_cases import case, parametrize


class CaseInvalidAttr:
    @case(tags=["base_public", "base"])
    @parametrize(attr=["name", "uuid"])
    def case_attr(self, attr: str) -> tuple[str, None]:
        return attr, None

    @case(tags=["create_extended"])
    @parametrize(len=[0, 1, 2])
    def case_projects(self, len: int) -> tuple[list[UUID], str]:
        if len == 1:
            return [uuid4()], "Public images do not have linked projects"
        elif len == 2:
            i = uuid4()
            return [i, i], "There are multiple identical items"
        return [], "Projects are mandatory for private images"
