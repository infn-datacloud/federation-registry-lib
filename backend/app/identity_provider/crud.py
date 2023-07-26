from typing import Optional
from app.auth_method.schemas import AuthMethodCreate
from app.crud import CRUDBase
from app.identity_provider.models import (
    IdentityProvider,
)
from app.identity_provider.schemas import (
    IdentityProviderCreate,
    IdentityProviderUpdate,
)
from app.provider.models import Provider
from app.user_group.crud import user_group


class CRUDIdentityProvider(
    CRUDBase[IdentityProvider, IdentityProviderCreate, IdentityProviderUpdate]
):
    """"""

    def create(
        self,
        *,
        obj_in: IdentityProviderCreate,
        provider: Optional[Provider] = None,
        relationship: AuthMethodCreate = None,
        force: bool = False
    ) -> IdentityProvider:
        db_obj = super().create(obj_in=obj_in, force=force)
        if provider is not None and relationship is not None:
            db_obj.providers.connect(provider, relationship.dict())
        return db_obj

    def remove(self, *, db_obj: IdentityProvider) -> bool:
        for item in db_obj.user_groups.all():
            user_group.remove(item)
        return super().remove(db_obj=db_obj)


identity_provider = CRUDIdentityProvider(
    IdentityProvider, IdentityProviderCreate
)
