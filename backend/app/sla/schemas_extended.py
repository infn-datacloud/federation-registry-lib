from pydantic import Field
from typing import List

from app.identity_provider.schemas import IdentityProviderRead
from app.project.schemas import ProjectRead
from app.project.schemas_extended import QuotaReadExtended
from app.provider.schemas import ProviderRead
from app.sla.schemas import SLARead
from app.user_group.schemas import UserGroupRead


class ProjectReadExtended(ProjectRead):
    provider: ProviderRead
    quotas: List[QuotaReadExtended] = Field(default_factory=list)


class UserGroupReadExtended(UserGroupRead):
    identity_provider: IdentityProviderRead


class SLAReadExtended(SLARead):
    project: ProjectReadExtended
    user_group: UserGroupReadExtended
