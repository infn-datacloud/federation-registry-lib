from typing import Optional, Union

from app.crud import CRUDBase
from app.identity_provider.crud import identity_provider
from app.project.crud import project
from app.provider.models import Provider
from app.provider.schemas import (
    ProviderCreate,
    ProviderRead,
    ProviderReadPublic,
    ProviderReadShort,
    ProviderUpdate,
)
from app.provider.schemas_extended import (
    ProviderCreateExtended,
    ProviderReadExtended,
    ProviderReadExtendedPublic,
)
from app.region.crud import region


class CRUDProvider(
    CRUDBase[
        Provider,
        ProviderCreate,
        ProviderUpdate,
        ProviderRead,
        ProviderReadPublic,
        ProviderReadShort,
        ProviderReadExtended,
        ProviderReadExtendedPublic,
    ]
):
    """"""

    def create(self, *, obj_in: ProviderCreateExtended) -> Provider:
        db_obj = super().create(obj_in=obj_in, force=True)
        for item in obj_in.projects:
            project.create(obj_in=item, provider=db_obj)
        for item in obj_in.identity_providers:
            identity_provider.create(obj_in=item, provider=db_obj)
        for item in obj_in.regions:
            region.create(obj_in=item, provider=db_obj)
        return db_obj

    def remove(self, *, db_obj: Provider) -> bool:
        for item in db_obj.projects:
            project.remove(db_obj=item)
        for item in db_obj.regions:
            region.remove(db_obj=item, from_provider=True)
        for item in db_obj.identity_providers:
            if len(item.providers) == 1:
                identity_provider.remove(db_obj=item)
        result = super().remove(db_obj=db_obj)
        return result

    def update(
        self,
        *,
        db_obj: Provider,
        obj_in: Union[ProviderCreateExtended, ProviderUpdate],
        force: bool = False
    ) -> Optional[Provider]:
        if force:
            # Projects
            db_items = {db_item.uuid: db_item for db_item in db_obj.projects}
            for item in obj_in.projects:
                db_item = db_items.pop(str(item.uuid), None)
                if not db_item:
                    project.create(obj_in=item, provider=db_obj)
                else:
                    project.update(db_obj=db_item, obj_in=item, force=force)
            for db_item in db_items.values():
                project.remove(db_obj=db_item)

            # Identity providers
            db_items = {
                db_item.endpoint: db_item for db_item in db_obj.identity_providers
            }
            for item in obj_in.identity_providers:
                db_item = db_items.pop(item.endpoint, None)
                if not db_item:
                    identity_provider.create(obj_in=item, provider=db_obj)
                else:
                    identity_provider.update(
                        db_obj=db_item,
                        obj_in=item,
                        projects=db_obj.projects.all(),
                        force=force,
                    )
            for db_item in db_items.values():
                if len(db_item.providers) <= 1:
                    identity_provider.remove(db_obj=db_item)
                else:
                    db_obj.identity_providers.disconnect(db_item)

            # Regions
            db_items = {db_item.name: db_item for db_item in db_obj.regions}
            for item in obj_in.regions:
                db_item = db_items.pop(item.name, None)
                if db_item is None:
                    region.create(obj_in=item, provider=db_obj)
                else:
                    region.update(
                        db_obj=db_item,
                        obj_in=item,
                        projects=db_obj.projects.all(),
                        force=force,
                    )
            for db_item in db_items.values():
                region.remove(db_obj=db_item, from_provider=True)
        return super().update(
            db_obj=db_obj, obj_in=ProviderUpdate.parse_obj(obj_in), force=force
        )


provider = CRUDProvider(
    model=Provider,
    create_schema=ProviderCreate,
    read_schema=ProviderRead,
    read_public_schema=ProviderReadPublic,
    read_short_schema=ProviderReadShort,
    read_extended_schema=ProviderReadExtended,
    read_extended_public_schema=ProviderReadExtendedPublic,
)
