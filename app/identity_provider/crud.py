from app.crud import CRUDBase
from app.identity_provider.models import (
    IdentityProvider,
)
from app.identity_provider.schemas import (
    IdentityProviderCreate,
    IdentityProviderUpdate,
)
from app.user_group.crud import user_group


class CRUDIdentityProvider(
    CRUDBase[IdentityProvider, IdentityProviderCreate, IdentityProviderUpdate]
):
    """"""

    def remove(self, *, db_obj: IdentityProvider) -> bool:
        for item in db_obj.user_groups.all():
            user_group.remove(item)
        return super().remove(db_obj=db_obj)


identity_provider = CRUDIdentityProvider(
    IdentityProvider, IdentityProviderCreate
)
