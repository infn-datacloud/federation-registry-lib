from typing import List, Optional, Union

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
        self, *, obj_in: IdentityProviderCreateExtended, provider: Provider
    ) -> IdentityProvider:
        db_obj = super().create(obj_in=obj_in, force=False)
        db_obj.providers.connect(provider, obj_in.relationship.dict())
        for item in obj_in.user_groups:
            user_group.create(
                obj_in=item,
                identity_provider=db_obj,
                projects=provider.projects.all(),
            )
        return db_obj

    def remove(self, *, db_obj: IdentityProvider) -> bool:
        for item in db_obj.user_groups:
            user_group.remove(db_obj=item)
        return super().remove(db_obj=db_obj)

    def update(
        self,
        *,
        db_obj: IdentityProvider,
        obj_in: Union[IdentityProviderCreateExtended, IdentityProviderUpdate],
        projects: List[Project] = [],
        force: bool = False
    ) -> Optional[IdentityProvider]:
        if force:
            db_items = {db_item.name: db_item for db_item in db_obj.user_groups}
            for item in obj_in.user_groups:
                db_item = db_items.pop(item.name, None)
                if db_item is None:
                    user_group.create(
                        obj_in=item, identity_provider=db_obj, projects=projects
                    )
                else:
                    user_group.update(
                        db_obj=db_item, obj_in=item, projects=projects, force=force
                    )
            for db_item in db_items.values():
                user_group.remove(db_obj=db_item)
        return super().update(db_obj=db_obj, obj_in=obj_in, force=force)


identity_provider = CRUDIdentityProvider(
    model=IdentityProvider,
    create_schema=IdentityProviderCreate,
    read_schema=IdentityProviderRead,
    read_public_schema=IdentityProviderReadPublic,
    read_short_schema=IdentityProviderReadShort,
    read_extended_schema=IdentityProviderReadExtended,
    read_extended_public_schema=IdentityProviderReadExtendedPublic,
)
