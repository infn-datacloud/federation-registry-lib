from .models import IdentityProvider as IdentityProviderModel
from .schemas import IdentityProviderCreate, IdentityProviderPatch
from ..crud import CRUDBase


class CRUDIdentityProvider(
    CRUDBase[
        IdentityProviderModel, IdentityProviderCreate, IdentityProviderPatch
    ]
):
    """"""


identity_provider = CRUDIdentityProvider(IdentityProviderModel, IdentityProviderCreate)
