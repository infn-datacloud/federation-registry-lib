from typing import Literal, Optional
from uuid import uuid4

from pydantic import EmailStr
from pytest_cases import case, parametrize

from fed_reg.project.schemas import ProjectCreate
from fed_reg.provider.enum import ProviderStatus, ProviderType
from fed_reg.provider.schemas_extended import (
    IdentityProviderCreateExtended,
    RegionCreateExtended,
    SLACreateExtended,
)
from tests.create_dict import project_schema_dict, region_schema_dict, sla_schema_dict
from tests.utils import random_email, random_lower_string, random_url


class CaseAttr:
    @case(tags=["base_public", "base", "update"])
    def case_none(self) -> tuple[None, None]:
        return None, None

    @case(tags=["update"])
    @parametrize(attr=["name", "type"])
    def case_attr(self, attr: str) -> tuple[str, None]:
        return attr, None

    @case(tags=["base_public", "base"])
    def case_desc(self) -> tuple[Literal["description"], str]:
        return "description", random_lower_string()

    @case(tags=["base_public", "base"])
    @parametrize(value=(i for i in ProviderType))
    def case_provider_type(
        self, value: ProviderType
    ) -> tuple[Literal["type"], ProviderType]:
        return "type", value

    @case(tags=["base"])
    @parametrize(value=(True, False))
    def case_is_public(self, value: bool) -> tuple[Literal["is_public"], bool]:
        return "is_public", value

    @case(tags=["base"])
    @parametrize(value=(i for i in ProviderStatus))
    def case_provider_status(
        self, value: ProviderStatus
    ) -> tuple[Literal["status"], ProviderStatus]:
        return "status", value

    @case(tags=["base"])
    @parametrize(len=(0, 1, 2))
    def case_email_list(
        self, len: int
    ) -> tuple[Literal["support_emails"], Optional[list[EmailStr]]]:
        return "support_emails", [random_email() for _ in range(len)]

    @case(tags=["create_extended"])
    @parametrize(len=(0, 1, 2))
    def case_projects(
        self, len: int
    ) -> tuple[Literal["projects"], list[ProjectCreate]]:
        return "projects", [ProjectCreate(**project_schema_dict()) for _ in range(len)]

    @case(tags=["create_extended"])
    @parametrize(len=(0, 1, 2))
    def case_regions(
        self, len: int
    ) -> tuple[Literal["regions"], list[RegionCreateExtended]]:
        return "regions", [
            RegionCreateExtended(**region_schema_dict()) for _ in range(len)
        ]

    @case(tags=["create_extended"])
    @parametrize(len=(0, 1, 2))
    def case_identity_providers(
        self,
        identity_provider_create_ext_schema: IdentityProviderCreateExtended,
        len: int,
    ) -> tuple[Literal["identity_providers"], list[IdentityProviderCreateExtended]]:
        if len == 1:
            return "identity_providers", [identity_provider_create_ext_schema]
        elif len == 2:
            idp2 = identity_provider_create_ext_schema.copy()
            user_group = idp2.user_groups[0].copy()
            user_group.sla = SLACreateExtended(**sla_schema_dict(), project=uuid4())
            idp2.user_groups = [user_group]
            idp2.endpoint = random_url()
            return "identity_providers", [identity_provider_create_ext_schema, idp2]
        else:
            return "identity_providers", []
