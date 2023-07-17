from pydantic import Field
from typing import List

from app.identity_provider.schemas import IdentityProviderRead
from app.provider.schemas import ProviderRead
from app.user_group.schemas import UserGroupRead


class IdentityProviderReadExtended(IdentityProviderRead):
    user_groups: List[UserGroupRead] = Field(default_factory=list)
    providers: List[ProviderRead] = Field(default_factory=list)
