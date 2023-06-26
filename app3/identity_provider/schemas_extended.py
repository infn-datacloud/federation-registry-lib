from ..auth_method.schemas import AuthMethod, AuthMethodCreate
from ..identity_provider.schemas import (
    IdentityProvider,
    IdentityProviderCreate,
)


class IdentityProviderCreateExtended(IdentityProviderCreate):
    relationship: AuthMethodCreate


class IdentityProviderExtended(IdentityProvider):
    relationship: AuthMethod
