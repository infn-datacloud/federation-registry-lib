from pytest_cases import case, parametrize

from fedreg.project.models import Project
from tests.v1.models.utils import project_model_dict


class CaseAttr:
    @case(tags="projects")
    @parametrize(len=(1, 2))
    def case_projects(self, len: int) -> list[Project]:
        return [Project(**project_model_dict()).save() for _ in range(len)]
