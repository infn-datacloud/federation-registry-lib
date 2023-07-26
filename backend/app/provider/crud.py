from app.crud import CRUDBase
from app.flavor.crud import flavor
from app.identity_provider.crud import identity_provider
from app.image.crud import image
from app.location.crud import location
from app.project.crud import project
from app.provider.models import Provider
from app.provider.schemas import ProviderCreate, ProviderUpdate
from app.provider.schemas_extended import (
    ProviderCreateExtended,
)
from app.service.crud import service


class CRUDProvider(CRUDBase[Provider, ProviderCreate, ProviderUpdate]):
    """"""

    def create(
        self, *, obj_in: ProviderCreateExtended, force: bool = False
    ) -> Provider:
        db_obj = super().create(obj_in=obj_in, force=force)
        if obj_in.location is not None:
            location.create(obj_in=obj_in.location, provider=db_obj)
        for item in obj_in.identity_providers:
            identity_provider.create(
                obj_in=item, provider=db_obj, relationship=item.relationship
            )
        for item in obj_in.flavors:
            flavor.create(obj_in=item, provider=db_obj, force=True)
        for item in obj_in.images:
            image.create(obj_in=item, provider=db_obj, force=True)
        for item in obj_in.projects:
            project.create(obj_in=item, provider=db_obj, force=True)
        for item in obj_in.services:
            service.create(obj_in=item, provider=db_obj, force=True)
        return db_obj

    def remove(self, *, db_obj: Provider) -> bool:
        for item in db_obj.flavors.all():
            flavor.remove(item)
        for item in db_obj.images.all():
            image.remove(item)
        for item in db_obj.projects.all():
            project.remove(item)
        for item in db_obj.services.all():
            service.remove(item)
        return super().remove(db_obj=db_obj)


provider = CRUDProvider(Provider, ProviderCreate)
