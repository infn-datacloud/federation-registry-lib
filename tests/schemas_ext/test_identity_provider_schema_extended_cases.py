from pytest_cases import case, parametrize

from fedreg.provider.models import Provider
from fedreg.user_group.models import UserGroup
from tests.models.utils import provider_model_dict, user_group_model_dict


class CaseAttr:
    @case(tags="providers")
    @parametrize(len=(1, 2))
    def case_providers(self, len: int) -> list[Provider]:
        return [Provider(**provider_model_dict()).save() for _ in range(len)]

    @case(tags="user_groups")
    @parametrize(len=(0, 1, 2))
    def case_user_groups(self, len: int) -> list[UserGroup]:
        return [UserGroup(**user_group_model_dict()).save() for _ in range(len)]
