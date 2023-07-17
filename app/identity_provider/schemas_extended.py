from pydantic import Field
from typing import List

from app.auth_method.schemas import AuthMethodRead
from app.identity_provider.schemas import IdentityProviderRead
from app.provider.schemas import ProviderRead
from app.user_group.schemas import UserGroupRead


class ProviderReadExtended(ProviderRead):
    relationship: AuthMethodRead


class IdentityProviderReadExtended(IdentityProviderRead):
    user_groups: List[UserGroupRead] = Field(default_factory=list)
    providers: List[ProviderReadExtended] = Field(default_factory=list)
