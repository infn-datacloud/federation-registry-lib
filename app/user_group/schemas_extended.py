from pydantic import Field
from typing import List

from app.identity_provider.schemas import IdentityProviderRead
from app.project.schemas import ProjectRead
from app.provider.schemas import ProviderRead
from app.sla.schemas import SLARead
from app.user_group.schemas import UserGroupRead


class ProjectReadExtended(ProjectRead):
    provider: ProviderRead


class SLAReadExtended(SLARead):
    project: ProjectRead


class UserGroupReadExtended(UserGroupRead):
    identity_provider: IdentityProviderRead = Field(default_factory=list)
    slas: List[SLAReadExtended] = Field(default_factory=list)
