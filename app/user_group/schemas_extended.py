from pydantic import Field
from typing import List

from app.user_group.schemas import UserGroupRead
from app.identity_provider.schemas import IdentityProviderRead
from app.project.schemas import ProjectRead


class UserGroupReadExtended(UserGroupRead):
    identity_provider: IdentityProviderRead = Field(default_factory=list)
    projects: List[ProjectRead] = Field(default_factory=list)
