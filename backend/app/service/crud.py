from typing import Any, Dict, List, Optional, Union

from app.crud import CRUDBase
from app.flavor.crud import flavor
from app.image.crud import image
from app.network.crud import network
from app.project.models import Project
from app.provider.schemas_extended import (
    BlockStorageServiceCreateExtended,
    ComputeServiceCreateExtended,
    NetworkServiceCreateExtended,
)
from app.quota.crud import block_storage_quota, compute_quota, quota
from app.region.models import Region
from app.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
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
    IdentityServiceCreate,
    IdentityServiceRead,
    IdentityServiceReadPublic,
    IdentityServiceReadShort,
    IdentityServiceUpdate,
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
    IdentityServiceReadExtended,
    IdentityServiceReadExtendedPublic,
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
            db_obj = block_storage_service.create(
                obj_in=obj_in, region=region, force=force
            )
        elif isinstance(obj_in, ComputeServiceCreate):
            db_obj = compute_service.create(obj_in=obj_in, region=region, force=force)
        elif isinstance(obj_in, IdentityServiceCreate):
            db_obj = identity_service.create(obj_in=obj_in, region=region, force=force)
        elif isinstance(obj_in, NetworkServiceCreate):
            db_obj = network_service.create(obj_in=obj_in, region=region, force=force)
        return db_obj

    def remove(self, *, db_obj: Service) -> bool:
        if isinstance(db_obj, BlockStorageService):
            return block_storage_service.remove(db_obj=db_obj)
        elif isinstance(db_obj, ComputeService):
            return compute_service.remove(db_obj=db_obj)
        elif isinstance(db_obj, IdentityService):
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
        elif isinstance(db_obj, IdentityService):
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

    def create(
        self,
        *,
        obj_in: BlockStorageServiceCreateExtended,
        region: Region,
        projects: List[Project],
    ) -> BlockStorageService:
        db_obj = super().create(obj_in=obj_in, force=True)
        db_obj.region.connect(region)
        for item in obj_in.quotas:
            db_projects = list(filter(lambda x: x.uuid == str(item.project), projects))
            if len(db_projects) == 1:
                block_storage_quota.create(
                    obj_in=item, service=db_obj, project=db_projects[0]
                )
        return db_obj

    def remove(self, *, db_obj: BlockStorageService) -> bool:
        for item in db_obj.quotas:
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

    def create(
        self,
        *,
        obj_in: ComputeServiceCreateExtended,
        region: Region,
        projects: List[Project],
    ) -> ComputeService:
        db_obj = super().create(obj_in=obj_in, force=True)
        db_obj.region.connect(region)
        for item in obj_in.flavors:
            item_projects = [str(i) for i in item.projects]
            db_projects = list(filter(lambda x: x.uuid in item_projects, projects))
            flavor.create(obj_in=item, service=db_obj, projects=db_projects)
        for item in obj_in.images:
            item_projects = [str(i) for i in item.projects]
            db_projects = list(filter(lambda x: x.uuid in item_projects, projects))
            image.create(obj_in=item, service=db_obj, projects=db_projects)
        for item in obj_in.quotas:
            db_projects = list(filter(lambda x: x.uuid == str(item.project), projects))
            if len(db_projects) == 1:
                compute_quota.create(
                    obj_in=item, service=db_obj, project=db_projects[0]
                )
        return db_obj

    def remove(self, *, db_obj: ComputeService) -> bool:
        for item in db_obj.quotas:
            quota.remove(db_obj=item)
        for item in db_obj.flavors:
            if len(item.services) == 1:
                flavor.remove(db_obj=item)
        for item in db_obj.images:
            if len(item.services) == 1:
                image.remove(db_obj=item)
        result = super().remove(db_obj=db_obj)
        return result


class CRUDIdentityService(
    CRUDBase[
        IdentityService,
        IdentityServiceCreate,
        IdentityServiceUpdate,
        IdentityServiceRead,
        IdentityServiceReadPublic,
        IdentityServiceReadShort,
        IdentityServiceReadExtended,
        IdentityServiceReadExtendedPublic,
    ]
):
    """"""

    def create(
        self, *, obj_in: IdentityServiceCreate, region: Region
    ) -> IdentityService:
        db_obj = super().create(obj_in=obj_in, force=True)
        db_obj.region.connect(region)
        return db_obj


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

    def create(
        self,
        *,
        obj_in: NetworkServiceCreateExtended,
        region: Region,
        projects: List[Project] = [],
    ) -> NetworkService:
        db_obj = super().create(obj_in=obj_in, force=True)
        db_obj.region.connect(region)
        for item in obj_in.networks:
            db_projects = list(filter(lambda x: x.uuid == str(item.project), projects))
            db_project = None
            if len(db_projects) == 1:
                db_project = db_projects[0]
            network.create(obj_in=item, service=db_obj, project=db_project)
        return db_obj

    def remove(self, *, db_obj: NetworkService) -> bool:
        for item in db_obj.networks:
            if len(item.services) == 1:
                network.remove(db_obj=item)
        result = super().remove(db_obj=db_obj)
        return result

    def update(
        self,
        *,
        db_obj: NetworkService,
        obj_in: Union[NetworkServiceCreateExtended, NetworkServiceUpdate],
        projects: List[Project] = [],
        force: bool = False,
    ) -> Optional[NetworkService]:
        edit = False
        if force:
            # Networks
            db_items = {db_item.uuid: db_item for db_item in db_obj.networks}
            for item in obj_in.networks:
                db_item = db_items.pop(str(item.uuid), None)
                db_projects = list(filter(lambda x: x.uuid == item.project, projects))
                if db_item is None:
                    project = None if len(db_projects) == 0 else db_projects[0]
                    network.create(obj_in=item, service=db_obj, project=project)
                    edit = True
                else:
                    updated_data = network.update(
                        db_obj=db_item, obj_in=item, projects=db_projects
                    )
                    if not edit and updated_data is not None:
                        edit = True
            for db_item in db_items.values():
                network.remove(db_obj=db_item)
                edit = True

        updated_data = super().update(
            db_obj=db_obj, obj_in=NetworkServiceUpdate.parse_obj(obj_in), force=force
        )
        return db_obj if edit else updated_data


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
identity_service = CRUDIdentityService(
    model=IdentityService,
    create_schema=IdentityServiceCreate,
    read_schema=IdentityServiceRead,
    read_public_schema=IdentityServiceReadPublic,
    read_short_schema=IdentityServiceReadShort,
    read_extended_schema=IdentityServiceReadExtended,
    read_extended_public_schema=IdentityServiceReadExtendedPublic,
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
