from typing import Any, Dict, Optional, Union

from app.crud import CRUDBase
from app.flavor.crud import flavor
from app.image.crud import image
from app.network.crud import network
from app.quota.crud import quota
from app.region.models import Region
from app.service.models import (
    BlockStorageService,
    ComputeService,
    KeystoneService,
    NetworkService,
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
    NetworkServiceCreate,
    NetworkServiceRead,
    NetworkServiceReadPublic,
    NetworkServiceReadShort,
    NetworkServiceUpdate,
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
    NetworkServiceReadExtended,
    NetworkServiceReadExtendedPublic,
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
        self, *, obj_in: ServiceCreate, region: Region, force: bool = False
    ) -> Service:
        if isinstance(obj_in, BlockStorageServiceCreate):
            db_obj = block_storage_service.create(obj_in=obj_in, force=force)
        elif isinstance(obj_in, ComputeServiceCreate):
            db_obj = compute_service.create(obj_in=obj_in, force=force)
        elif isinstance(obj_in, KeystoneServiceCreate):
            db_obj = identity_service.create(obj_in=obj_in, force=force)
        elif isinstance(obj_in, NetworkServiceCreate):
            db_obj = network_service.create(obj_in=obj_in, force=force)
        db_obj.region.connect(region)
        return db_obj

    def remove(self, *, db_obj: Service) -> bool:
        if isinstance(db_obj, BlockStorageService):
            return block_storage_service.remove(db_obj=db_obj)
        elif isinstance(db_obj, ComputeService):
            return compute_service.remove(db_obj=db_obj)
        elif isinstance(db_obj, KeystoneService):
            return identity_service.remove(db_obj=db_obj)
        elif isinstance(db_obj, NetworkService):
            return network_service.remove(db_obj=db_obj)

    def update(
        self, *, db_obj: Service, obj_in: Union[ServiceUpdate, Dict[str, Any]]
    ) -> Optional[Service]:
        if isinstance(db_obj, BlockStorageService):
            return block_storage_service.update(db_obj=db_obj, obj_in=obj_in)
        elif isinstance(db_obj, ComputeService):
            return compute_service.update(db_obj=db_obj, obj_in=obj_in)
        elif isinstance(db_obj, KeystoneService):
            return identity_service.update(db_obj=db_obj, obj_in=obj_in)
        elif isinstance(db_obj, NetworkService):
            return network_service.update(db_obj=db_obj, obj_in=obj_in)


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

    def remove(self, *, db_obj: BlockStorageService) -> bool:
        for item in db_obj.quotas.all():
            quota.remove(db_obj=item)
        return super().remove(db_obj=db_obj)


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

    def remove(self, *, db_obj: ComputeService) -> bool:
        for item in db_obj.quotas.all():
            quota.remove(db_obj=item)
        result = super().remove(db_obj=db_obj)
        for item in db_obj.flavors.all():
            if len(item.services.all()) == 0:
                flavor.remove(db_obj=item)
        for item in db_obj.images.all():
            if len(item.services.all()) == 0:
                image.remove(db_obj=item)
        return result


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


class CRUDNetworkService(
    CRUDBase[
        NetworkService,
        NetworkServiceCreate,
        NetworkServiceUpdate,
        NetworkServiceRead,
        NetworkServiceReadPublic,
        NetworkServiceReadShort,
        NetworkServiceReadExtended,
        NetworkServiceReadExtendedPublic,
    ]
):
    """"""

    def remove(self, *, db_obj: NetworkService) -> bool:
        result = super().remove(db_obj=db_obj)
        for item in db_obj.networks.all():
            if len(item.services.all()) == 0:
                network.remove(db_obj=item)
        return result


service = CRUDService(
    model=Service,
    create_schema=ServiceCreate,
    read_schema=ServiceRead,
    read_public_schema=ServiceReadPublic,
    read_short_schema=ServiceReadShort,
    read_extended_schema=None,
    read_extended_public_schema=None,
)
compute_service = CRUDComputeService(
    model=ComputeService,
    create_schema=ComputeServiceCreate,
    read_schema=ComputeServiceRead,
    read_public_schema=ComputeServiceReadPublic,
    read_short_schema=ComputeServiceReadShort,
    read_extended_schema=ComputeServiceReadExtended,
    read_extended_public_schema=ComputeServiceReadExtendedPublic,
)
block_storage_service = CRUDBlockStorageService(
    model=BlockStorageService,
    create_schema=BlockStorageServiceCreate,
    read_schema=BlockStorageServiceRead,
    read_public_schema=BlockStorageServiceReadPublic,
    read_short_schema=BlockStorageServiceReadShort,
    read_extended_schema=BlockStorageServiceReadExtended,
    read_extended_public_schema=BlockStorageServiceReadExtendedPublic,
)
identity_service = CRUDKeystoneService(
    model=KeystoneService,
    create_schema=KeystoneServiceCreate,
    read_schema=KeystoneServiceRead,
    read_public_schema=KeystoneServiceReadPublic,
    read_short_schema=KeystoneServiceReadShort,
    read_extended_schema=KeystoneServiceReadExtended,
    read_extended_public_schema=KeystoneServiceReadExtendedPublic,
)
network_service = CRUDNetworkService(
    model=NetworkService,
    create_schema=NetworkServiceCreate,
    read_schema=NetworkServiceRead,
    read_public_schema=NetworkServiceReadPublic,
    read_short_schema=NetworkServiceReadShort,
    read_extended_schema=NetworkServiceReadExtended,
    read_extended_public_schema=NetworkServiceReadExtendedPublic,
)
