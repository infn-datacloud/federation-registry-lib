from typing import Literal
from uuid import uuid4

from pytest_cases import case

from fed_reg.provider.schemas_extended import UserGroupCreateExtended
from tests.utils import random_lower_string


class CaseInvalidAttr:
    @case(tags=["base_public", "base"])
    def case_endpoint(self) -> tuple[Literal["endpoint"], None]:
        return "endpoint", None

    @case(tags=["base"])
    def case_group_claim(self) -> tuple[Literal["group_claim"], None]:
        return "group_claim", None

    @case(tags=["create_extended"])
    def case_missing_relationship(self) -> tuple[Literal["relationship"], None, None]:
        return "relationship", None, None

    @case(tags=["create_extended"])
    def case_no_user_groups(self) -> tuple[Literal["user_groups"], list, str]:
        return (
            "user_groups",
            [],
            "Identity provider's user group list can't be empty",
        )

    @case(tags=["create_extended"])
    def case_dup_user_groups(
        self, user_group_create_ext_schema: UserGroupCreateExtended
    ) -> tuple[Literal["user_groups"], list[UserGroupCreateExtended], str]:
        return (
            "user_groups",
            [user_group_create_ext_schema, user_group_create_ext_schema],
            "There are multiple items with identical name",
        )

    @case(tags=["create_extended"])
    def case_dup_sla_doc_uuid(
        self, user_group_create_ext_schema: UserGroupCreateExtended
    ) -> tuple[Literal["user_groups"], list[UserGroupCreateExtended], str]:
        user_group2 = user_group_create_ext_schema.copy()
        user_group2.name = random_lower_string()
        return (
            "user_groups",
            [user_group_create_ext_schema, user_group2],
            "already used by another user group",
        )

    @case(tags=["create_extended"])
    def case_dup_sla_project(
        self, user_group_create_ext_schema: UserGroupCreateExtended
    ) -> tuple[Literal["user_groups"], list[UserGroupCreateExtended], str]:
        user_group2 = user_group_create_ext_schema.copy()
        user_group2.name = random_lower_string()
        user_group2.sla = user_group_create_ext_schema.sla.copy()
        user_group2.sla.doc_uuid = uuid4()
        return (
            "user_groups",
            [user_group_create_ext_schema, user_group2],
            "already used by another SLA",
        )
