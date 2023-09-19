from typing import Any, Dict, Optional, Union

from app.crud import CRUDBase
from app.provider.models import Provider
from app.quota.crud import quota
from app.service.models import (
    BlockStorageService,
    ComputeService,
    KeystoneService,
    Service,
)
from app.service.schemas import (
    BlockStorageServiceCreate,
    BlockStorageServiceRead,
    BlockStorageServiceReadPublic,
    BlockStorageServiceReadShort,
    BlockStorageServiceUpdate,
    ComputeServiceCreate,
    ComputeServiceRead,
    ComputeServiceReadPublic,
    ComputeServiceReadShort,
    ComputeServiceUpdate,
    KeystoneServiceCreate,
    KeystoneServiceRead,
    KeystoneServiceReadPublic,
    KeystoneServiceReadShort,
    KeystoneServiceUpdate,
    ServiceCreate,
    ServiceRead,
    ServiceReadPublic,
    ServiceReadShort,
    ServiceUpdate,
)
from app.service.schemas_extended import (
    BlockStorageServiceReadExtended,
    BlockStorageServiceReadExtendedPublic,
    ComputeServiceReadExtended,
    ComputeServiceReadExtendedPublic,
    KeystoneServiceReadExtended,
    KeystoneServiceReadExtendedPublic,
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
        if isinstance(obj_in, ComputeServiceCreate):
            db_obj = nova_service.create(obj_in=obj_in, force=force)
        elif isinstance(obj_in, BlockStorageServiceCreate):
            db_obj = cinder_service.create(obj_in=obj_in, force=force)
        elif isinstance(obj_in, KeystoneServiceCreate):
            db_obj = keystone_service.create(obj_in=obj_in, force=force)
        db_obj.provider.connect(provider)
        return db_obj

    def remove(self, *, db_obj: Service) -> bool:
        for item in db_obj.quotas.all():
            quota.remove(item)
        if isinstance(db_obj, ComputeService):
            return nova_service.remove(db_obj=db_obj)
        elif isinstance(db_obj, BlockStorageService):
            return cinder_service.remove(db_obj=db_obj)
        elif isinstance(db_obj, KeystoneService):
            return keystone_service.remove(db_obj=db_obj)

    def update(
        self, *, db_obj: Service, obj_in: Union[ServiceUpdate, Dict[str, Any]]
    ) -> Optional[Service]:
        if isinstance(db_obj, ComputeService):
            return nova_service.update(db_obj=db_obj, obj_in=obj_in)
        elif isinstance(db_obj, BlockStorageService):
            return cinder_service.update(db_obj=db_obj, obj_in=obj_in)
        elif isinstance(db_obj, KeystoneService):
            return keystone_service.update(db_obj=db_obj, obj_in=obj_in)


class CRUDComputeService(
    CRUDBase[
        ComputeService,
        ComputeServiceCreate,
        ComputeServiceUpdate,
        ComputeServiceRead,
        ComputeServiceReadPublic,
        ComputeServiceReadShort,
        ComputeServiceReadExtended,
        ComputeServiceReadExtendedPublic,
    ]
):
    """"""


class CRUDBlockStorageService(
    CRUDBase[
        BlockStorageService,
        BlockStorageServiceCreate,
        BlockStorageServiceUpdate,
        BlockStorageServiceRead,
        BlockStorageServiceReadPublic,
        BlockStorageServiceReadShort,
        BlockStorageServiceReadExtended,
        BlockStorageServiceReadExtendedPublic,
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
nova_service = CRUDComputeService(
    model=ComputeService,
    create_schema=ComputeServiceCreate,
    read_schema=ComputeServiceRead,
    read_public_schema=ComputeServiceReadPublic,
    read_short_schema=ComputeServiceReadShort,
    read_extended_schema=ComputeServiceReadExtended,
    read_extended_public_schema=ComputeServiceReadExtendedPublic,
)
cinder_service = CRUDBlockStorageService(
    model=BlockStorageService,
    create_schema=BlockStorageServiceCreate,
    read_schema=BlockStorageServiceRead,
    read_public_schema=BlockStorageServiceReadPublic,
    read_short_schema=BlockStorageServiceReadShort,
    read_extended_schema=BlockStorageServiceReadExtended,
    read_extended_public_schema=BlockStorageServiceReadExtendedPublic,
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
