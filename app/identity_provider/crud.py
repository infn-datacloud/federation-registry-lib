from app.identity_provider.models import (
    IdentityProvider ,
)
from app.identity_provider.schemas import (
    IdentityProviderCreate,
    IdentityProviderUpdate,
)
from app.crud import CRUDBase


class CRUDIdentityProvider(
    CRUDBase[
        IdentityProvider, IdentityProviderCreate, IdentityProviderUpdate
    ]
):
    """"""


identity_provider = CRUDIdentityProvider(
    IdentityProvider, IdentityProviderCreate
)
