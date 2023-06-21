from ..nodes.identity_provider import IdentityProvider, IdentityProviderCreate
from ..relationships.auth_method import AuthMethod, AuthMethodCreate


class IdentityProviderCreateExtended(IdentityProviderCreate):
    relationship: AuthMethodCreate


class IdentityProviderExtended(IdentityProvider):
    relationship: AuthMethod
