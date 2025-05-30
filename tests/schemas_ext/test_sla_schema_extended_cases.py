from pytest_cases import case, parametrize

from fedreg.project.models import Project
from fedreg.provider.models import Provider
from tests.models.utils import project_model_dict, provider_model_dict


class CaseAttr:
    @case(tags="projects")
    @parametrize(len=(1, 2))
    def case_projects(self, len: int) -> list[Project]:
        projects = []
        for _ in range(len):
            project = Project(**project_model_dict()).save()
            provider = Provider(**provider_model_dict()).save()
            project.provider.connect(provider)
            projects.append(project)
        return projects
