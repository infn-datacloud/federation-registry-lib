from ..auth_method.schemas import (
    AuthMethod,
    AuthMethodCreate,
    AuthMethodUpdate,
)
from ..identity_provider.schemas import (
    IdentityProvider,
    IdentityProviderCreate,
    IdentityProviderUpdate,
)


class IdentityProviderCreateExtended(IdentityProviderCreate):
    relationship: AuthMethodCreate


class IdentityProviderUpdateExtended(IdentityProviderUpdate):
    relationship: AuthMethodUpdate


class IdentityProviderExtended(IdentityProvider):
    relationship: AuthMethod
