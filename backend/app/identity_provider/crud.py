from typing import List, Optional

from app.auth_method.schemas import AuthMethodCreate
from app.crud import CRUDBase
from app.identity_provider.models import IdentityProvider
from app.identity_provider.schemas import (
    IdentityProviderCreate,
    IdentityProviderRead,
    IdentityProviderReadPublic,
    IdentityProviderReadShort,
    IdentityProviderUpdate,
)
from app.identity_provider.schemas_extended import (
    IdentityProviderReadExtended,
    IdentityProviderReadExtendedPublic,
)
from app.project.models import Project
from app.provider.models import Provider
from app.provider.schemas_extended import IdentityProviderCreateExtended
from app.user_group.crud import user_group


class CRUDIdentityProvider(
    CRUDBase[
        IdentityProvider,
        IdentityProviderCreate,
        IdentityProviderUpdate,
        IdentityProviderRead,
        IdentityProviderReadPublic,
        IdentityProviderReadShort,
        IdentityProviderReadExtended,
        IdentityProviderReadExtendedPublic,
    ]
):
    """"""

    def create(
        self,
        *,
        obj_in: IdentityProviderCreateExtended,
        projects: List[Project],
        provider: Optional[Provider] = None,
        relationship: AuthMethodCreate = None,
        force: bool = False
    ) -> IdentityProvider:
        db_obj = super().create(obj_in=obj_in, force=force)
        if provider is not None and relationship is not None:
            db_obj.providers.connect(provider, relationship.dict())
        for item in obj_in.user_groups:
            user_group.create(obj_in=item, identity_provider=db_obj, projects=projects)
        return db_obj

    def remove(self, *, db_obj: IdentityProvider) -> bool:
        for item in db_obj.user_groups:
            user_group.remove(db_obj=item)
        return super().remove(db_obj=db_obj)


identity_provider = CRUDIdentityProvider(
    model=IdentityProvider,
    create_schema=IdentityProviderCreate,
    read_schema=IdentityProviderRead,
    read_public_schema=IdentityProviderReadPublic,
    read_short_schema=IdentityProviderReadShort,
    read_extended_schema=IdentityProviderReadExtended,
    read_extended_public_schema=IdentityProviderReadExtendedPublic,
)
