from typing import Literal
from uuid import uuid4

from pytest_cases import case, parametrize

from fed_reg.provider.schemas_extended import SLACreateExtended, UserGroupCreateExtended
from tests.create_dict import sla_schema_dict, user_group_schema_dict
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "base", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["update"])
    def case_endpoint(self) -> tuple[Literal["endpoint"], None]:
        return "endpoint", None

    @case(tags=["update"])
    def case_no_group_claim(self) -> tuple[Literal["group_claim"], None]:
        return "group_claim", None

    @case(tags=["base_public", "base"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @case(tags=["base"])
    def case_group_claim(self) -> tuple[Literal["group_claim"], str]:
        return "group_claim", random_lower_string()

    @case(tags=["create_extended"])
    @parametrize(len=(1, 2))
    def case_user_groups(
        self, user_group_create_ext_schema: UserGroupCreateExtended, len: int
    ) -> list[UserGroupCreateExtended]:
        if len == 1:
            return [user_group_create_ext_schema]
        else:
            return [
                user_group_create_ext_schema,
                UserGroupCreateExtended(
                    **user_group_schema_dict(),
                    sla=SLACreateExtended(**sla_schema_dict(), project=uuid4()),
                ),
            ]
