from typing import Any, Dict, Optional, Union

from app.crud import CRUDBase
from app.provider.models import Provider
from app.quota.crud import quota
from app.service.models import CinderService, KeystoneService, NovaService, Service
from app.service.schemas import (
    CinderServiceCreate,
    CinderServiceRead,
    CinderServiceReadPublic,
    CinderServiceReadShort,
    CinderServiceUpdate,
    KeystoneServiceCreate,
    KeystoneServiceRead,
    KeystoneServiceReadPublic,
    KeystoneServiceReadShort,
    KeystoneServiceUpdate,
    NovaServiceCreate,
    NovaServiceRead,
    NovaServiceReadPublic,
    NovaServiceReadShort,
    NovaServiceUpdate,
    ServiceCreate,
    ServiceRead,
    ServiceReadPublic,
    ServiceReadShort,
    ServiceUpdate,
)
from app.service.schemas_extended import (
    CinderServiceReadExtended,
    CinderServiceReadExtendedPublic,
    KeystoneServiceReadExtended,
    KeystoneServiceReadExtendedPublic,
    NovaServiceReadExtended,
    NovaServiceReadExtendedPublic,
)


class CRUDService(
    CRUDBase[
        Service,
        ServiceCreate,
        ServiceUpdate,
        ServiceRead,
        ServiceReadPublic,
        ServiceReadShort,
        None,
        None,
    ]
):
    """"""

    def create(
        self, *, obj_in: ServiceCreate, provider: Provider, force: bool = False
    ) -> Service:
        if isinstance(obj_in, NovaServiceCreate):
            db_obj = nova_service.create(obj_in=obj_in, force=force)
        elif isinstance(obj_in, CinderServiceCreate):
            db_obj = cinder_service.create(obj_in=obj_in, force=force)
        elif isinstance(obj_in, KeystoneServiceCreate):
            db_obj = keystone_service.create(obj_in=obj_in, force=force)
        db_obj.provider.connect(provider)
        return db_obj

    def remove(self, *, db_obj: Service) -> bool:
        if isinstance(db_obj, NovaService):
            return nova_service.remove(db_obj=db_obj)
        elif isinstance(db_obj, CinderService):
            return cinder_service.remove(db_obj=db_obj)
        elif isinstance(db_obj, KeystoneService):
            return keystone_service.remove(db_obj=db_obj)

    def update(
        self, *, db_obj: Service, obj_in: Union[ServiceUpdate, Dict[str, Any]]
    ) -> Optional[Service]:
        if isinstance(db_obj, NovaService):
            return nova_service.update(db_obj=db_obj, obj_in=obj_in)
        elif isinstance(db_obj, CinderService):
            return cinder_service.update(db_obj=db_obj, obj_in=obj_in)
        elif isinstance(db_obj, KeystoneService):
            return keystone_service.update(db_obj=db_obj, obj_in=obj_in)


class CRUDNovaService(
    CRUDBase[
        NovaService,
        NovaServiceCreate,
        NovaServiceUpdate,
        NovaServiceRead,
        NovaServiceReadPublic,
        NovaServiceReadShort,
        NovaServiceReadExtended,
        NovaServiceReadExtendedPublic,
    ]
):
    """"""

    def remove(self, *, db_obj: NovaService) -> bool:
        for item in db_obj.num_cpu_quotas.all():
            quota.remove(item)
        for item in db_obj.ram_quotas.all():
            quota.remove(item)
        return super().remove(db_obj=db_obj)


class CRUDCinderService(
    CRUDBase[
        CinderService,
        CinderServiceCreate,
        CinderServiceUpdate,
        CinderServiceRead,
        CinderServiceReadPublic,
        CinderServiceReadShort,
        CinderServiceReadExtended,
        CinderServiceReadExtendedPublic,
    ]
):
    """"""


class CRUDKeystoneService(
    CRUDBase[
        KeystoneService,
        KeystoneServiceCreate,
        KeystoneServiceUpdate,
        KeystoneServiceRead,
        KeystoneServiceReadPublic,
        KeystoneServiceReadShort,
        KeystoneServiceReadExtended,
        KeystoneServiceReadExtendedPublic,
    ]
):
    """"""


service = CRUDService(
    model=Service,
    create_schema=ServiceCreate,
    read_schema=ServiceRead,
    read_public_schema=ServiceReadPublic,
    read_short_schema=ServiceReadShort,
    read_extended_schema=None,
    read_extended_public_schema=None,
)
nova_service = CRUDNovaService(
    model=NovaService,
    create_schema=NovaServiceCreate,
    read_schema=NovaServiceRead,
    read_public_schema=NovaServiceReadPublic,
    read_short_schema=NovaServiceReadShort,
    read_extended_schema=NovaServiceReadExtended,
    read_extended_public_schema=NovaServiceReadExtendedPublic,
)
cinder_service = CRUDCinderService(
    model=CinderService,
    create_schema=CinderServiceCreate,
    read_schema=CinderServiceRead,
    read_public_schema=CinderServiceReadPublic,
    read_short_schema=CinderServiceReadShort,
    read_extended_schema=CinderServiceReadExtended,
    read_extended_public_schema=CinderServiceReadExtendedPublic,
)
keystone_service = CRUDKeystoneService(
    model=KeystoneService,
    create_schema=KeystoneServiceCreate,
    read_schema=KeystoneServiceRead,
    read_public_schema=KeystoneServiceReadPublic,
    read_short_schema=KeystoneServiceReadShort,
    read_extended_schema=KeystoneServiceReadExtended,
    read_extended_public_schema=KeystoneServiceReadExtendedPublic,
)
