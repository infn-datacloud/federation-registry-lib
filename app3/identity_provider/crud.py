from .models import IdentityProvider as IdentityProviderModel
from .schemas import IdentityProviderCreate, IdentityProviderUpdate
from ..crud import CRUDBase


class CRUDIdentityProvider(
    CRUDBase[
        IdentityProviderModel, IdentityProviderCreate, IdentityProviderUpdate
    ]
):
    """"""


identity_provider = CRUDIdentityProvider(IdentityProviderModel, IdentityProviderCreate)
