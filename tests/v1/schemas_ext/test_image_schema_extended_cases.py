from pytest_cases import case, parametrize

from fedreg.project.models import Project
from fedreg.service.enum import ServiceType
from fedreg.service.models import ComputeService
from tests.v1.models.utils import project_model_dict, service_model_dict


class CaseAttr:
    @case(tags="services")
    @parametrize(len=(1, 2))
    def case_services(self, len: int) -> list[ComputeService]:
        return [
            ComputeService(**service_model_dict(ServiceType.COMPUTE)).save()
            for _ in range(len)
        ]

    @case(tags="projects")
    @parametrize(len=(1, 2))
    def case_projects(self, len: int) -> list[Project]:
        return [Project(**project_model_dict()).save() for _ in range(len)]
