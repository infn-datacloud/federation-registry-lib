from pydantic import Field
from typing import List

from ..identity_provider.schemas import IdentityProviderRead
from ..provider.schemas import ProviderRead
from ..user_group.schemas import UserGroupRead


class IdentityProviderReadExtended(IdentityProviderRead):
    user_groups: List[UserGroupRead] = Field(default_factory=list)
    providers: List[ProviderRead] = Field(default_factory=list)
