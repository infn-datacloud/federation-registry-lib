from pytest_cases import case, parametrize

from fedreg.v1.region.models import Region
from tests.v1.models.utils import region_model_dict


class CaseAttr:
    @case(tags="regions")
    @parametrize(len=(1, 2))
    def case_regions(self, len: int) -> list[Region]:
        return [Region(**region_model_dict()).save() for _ in range(len)]
