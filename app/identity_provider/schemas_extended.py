from ..auth_method.schemas import (
    AuthMethodCreate,
    AuthMethodRead,
    AuthMethodUpdate,
)
from ..identity_provider.schemas import (
    IdentityProviderCreate,
    IdentityProviderRead,
    IdentityProviderUpdate,
)


class IdentityProviderCreateExtended(IdentityProviderCreate):
    relationship: AuthMethodCreate


class IdentityProviderUpdateExtended(IdentityProviderUpdate):
    relationship: AuthMethodUpdate


class IdentityProviderReadExtended(IdentityProviderRead):
    relationship: AuthMethodRead
