from typing import List, Union

from app.provider.models import Provider 
from app.provider.schemas import ProviderCreate, ProviderUpdate
from app.provider.schemas_extended import (
    ProviderCreateExtended,
    IdentityProviderCreateExtended,
)
from app.crud import CRUDBase
from app.flavor.crud import flavor
from app.flavor.schemas import FlavorCreate
from app.identity_provider.crud import identity_provider
from app.image.crud import image
from app.image.schemas import ImageCreate
from app.location.crud import location
from app.location.schemas import LocationCreate
from app.project.crud import project
from app.project.schemas import ProjectCreate
from app.service.crud import (
    nova_service,
    mesos_service,
    chronos_service,
    marathon_service,
    kubernetes_service,
    rucio_service,
    onedata_service,
)
from app.service.schemas import (
    ChronosServiceCreate,
    KubernetesServiceCreate,
    MarathonServiceCreate,
    MesosServiceCreate,
    NovaServiceCreate,
    OneDataServiceCreate,
    RucioServiceCreate,
)


class CRUDProvider(CRUDBase[Provider, ProviderCreate, ProviderUpdate]):
    """"""

    def create_and_connect_flavors(
        self,
        *,
        db_obj: Provider,
        new_items: List[FlavorCreate],
    ) -> None:
        for flv in new_items:
            db_flavor = flavor.create(obj_in=flv, force=True)
            db_obj.flavors.connect(db_flavor)

    def create_and_connect_identity_providers(
        self,
        *,
        db_obj: Provider,
        new_items: List[IdentityProviderCreateExtended],
    ) -> None:
        for idp in new_items:
            db_identity_provider = identity_provider.create(obj_in=idp)
            db_obj.identity_providers.connect(
                db_identity_provider, idp.relationship.dict()
            )

    def create_and_connect_images(
        self,
        *,
        db_obj: Provider,
        new_items: List[ImageCreate],
    ) -> None:
        for img in new_items:
            db_image = image.create(obj_in=img, force=True)
            db_obj.images.connect(db_image)

    def create_and_connect_location(
        self, *, db_obj: Provider, loc: LocationCreate
    ) -> None:
        db_location = location.create(obj_in=loc)
        db_obj.location.connect(db_location)

    def create_and_connect_projects(
        self,
        *,
        db_obj: Provider,
        new_items: List[ProjectCreate],
    ) -> None:
        for proj in new_items:
            db_project = project.create(obj_in=proj, force=True)
            db_obj.projects.connect(db_project)

    def create_and_connect_services(
        self,
        *,
        db_obj: Provider,
        new_items: List[
            Union[
                ChronosServiceCreate,
                KubernetesServiceCreate,
                MarathonServiceCreate,
                MesosServiceCreate,
                NovaServiceCreate,
                OneDataServiceCreate,
                RucioServiceCreate,
            ]
        ],
    ) -> None:
        for obj_in in new_items:
            if isinstance(obj_in, NovaServiceCreate):
                db_service = nova_service.create(obj_in=obj_in, force=True)
            elif isinstance(obj_in, MesosServiceCreate):
                db_service = mesos_service.create(obj_in=obj_in, force=True)
            elif isinstance(obj_in, ChronosServiceCreate):
                db_service = chronos_service.create(obj_in=obj_in, force=True)
            elif isinstance(obj_in, MarathonServiceCreate):
                db_service = marathon_service.create(obj_in=obj_in, force=True)
            elif isinstance(obj_in, KubernetesServiceCreate):
                db_service = kubernetes_service.create(
                    obj_in=obj_in, force=True
                )
            elif isinstance(obj_in, RucioServiceCreate):
                db_service = rucio_service.create(obj_in=obj_in, force=True)
            elif isinstance(obj_in, OneDataServiceCreate):
                db_service = onedata_service.create(obj_in=obj_in, force=True)
            db_obj.services.connect(db_service)

    def create_with_all(
        self, *, obj_in: ProviderCreateExtended
    ) -> Provider:
        db_obj = self.create(obj_in=obj_in)
        if obj_in.location is not None:
            self.create_and_connect_location(
                db_obj=db_obj, loc=obj_in.location
            )
        self.create_and_connect_flavors(
            db_obj=db_obj, new_items=obj_in.flavors
        )
        self.create_and_connect_identity_providers(
            db_obj=db_obj, new_items=obj_in.identity_providers
        )
        self.create_and_connect_images(db_obj=db_obj, new_items=obj_in.images)
        self.create_and_connect_projects(
            db_obj=db_obj, new_items=obj_in.projects
        )
        self.create_and_connect_services(
            db_obj=db_obj, new_items=obj_in.services
        )
        return db_obj


provider = CRUDProvider(Provider, ProviderCreate)