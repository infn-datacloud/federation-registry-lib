from app.identity_provider.models import (
    IdentityProvider as IdentityProviderModel,
)
from app.identity_provider.schemas import (
    IdentityProviderCreate,
    IdentityProviderUpdate,
)
from app.crud import CRUDBase


class CRUDIdentityProvider(
    CRUDBase[
        IdentityProviderModel, IdentityProviderCreate, IdentityProviderUpdate
    ]
):
    """"""


identity_provider = CRUDIdentityProvider(
    IdentityProviderModel, IdentityProviderCreate
)
