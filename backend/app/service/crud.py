from typing import List, Optional, Union

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
from app.quota.crud import block_storage_quota, compute_quota
from app.region.models import Region
from app.service.models import (
    BlockStorageService,
    ComputeService,
    IdentityService,
    NetworkService,
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
    """Block Storage Service Create, Read, Update and Delete operations."""

    def create(
        self,
        *,
        obj_in: BlockStorageServiceCreateExtended,
        region: Region,
        projects: List[Project] = None,
    ) -> BlockStorageService:
        """Create a new Block Storage Service.

        Connect the service to the given region and create all relative quotas. Filter
        projects based on received ones and target one. It must be exactly one.
        """
        if projects is None:
            projects = []
        db_obj = super().create(obj_in=obj_in)
        db_obj.region.connect(region)
        for item in obj_in.quotas:
            db_projects = list(filter(lambda x: x.uuid == item.project, projects))
            if len(db_projects) == 1:
                block_storage_quota.create(
                    obj_in=item, service=db_obj, project=db_projects[0]
                )
        return db_obj

    def remove(self, *, db_obj: BlockStorageService) -> bool:
        """Delete an existing service and all its relationships.

        At first delete its quotas. Finally delete the service.
        """
        for item in db_obj.quotas:
            block_storage_quota.remove(db_obj=item)
        return super().remove(db_obj=db_obj)

    def update(
        self,
        *,
        db_obj: BlockStorageService,
        obj_in: Union[BlockStorageServiceCreateExtended, BlockStorageServiceUpdate],
        projects: List[Project] = None,
        force: bool = False,
    ) -> Optional[BlockStorageService]:
        """Update Block Storage Service attributes.

        By default do not update relationships or default values. If force is True,
        update linked quotas and apply default values when explicit.
        """
        if projects is None:
            projects = []
        edit = False
        if force:
            edit = self.__update_quotas(
                db_obj=db_obj, obj_in=obj_in, provider_projects=projects
            )

        if isinstance(obj_in, BlockStorageServiceCreateExtended):
            obj_in = BlockStorageServiceUpdate.parse_obj(obj_in)

        update_data = super().update(db_obj=db_obj, obj_in=obj_in, force=force)
        return db_obj if edit else update_data

    def __update_quotas(
        self,
        *,
        db_obj: BlockStorageService,
        obj_in: BlockStorageServiceCreateExtended,
        provider_projects: List[Project],
    ) -> bool:
        """Update service linked quotas.

        Connect new quotas not already connect, leave untouched already linked ones and
        delete old ones no more connected to the service.

        Split quotas in per_user and total. For each one of them, check the linked
        project. If the project already has a quota of that type, update that quota with
        the new received values.
        """
        edit = False

        db_items_per_user = {
            db_item.project.single().uuid: db_item
            for db_item in filter(lambda x: x.per_user, db_obj.quotas)
        }
        db_items_total = {
            db_item.project.single().uuid: db_item
            for db_item in filter(lambda x: not x.per_user, db_obj.quotas)
        }
        db_projects = {db_item.uuid: db_item for db_item in provider_projects}

        for item in obj_in.quotas:
            if item.per_user:
                db_item = db_items_per_user.pop(item.project, None)
                if not db_item:
                    block_storage_quota.create(
                        obj_in=item,
                        service=db_obj,
                        project=db_projects.get(item.project),
                    )
                    edit = True
                else:
                    updated_data = block_storage_quota.update(
                        db_obj=db_item,
                        obj_in=item,
                        projects=provider_projects,
                        force=True,
                    )
                    if not edit and updated_data is not None:
                        edit = True
            else:
                db_item = db_items_total.pop(item.project, None)
                if not db_item:
                    block_storage_quota.create(
                        obj_in=item,
                        service=db_obj,
                        project=db_projects.get(item.project),
                    )
                    edit = True
                else:
                    updated_data = block_storage_quota.update(
                        db_obj=db_item,
                        obj_in=item,
                        projects=provider_projects,
                        force=True,
                    )
                    if not edit and updated_data is not None:
                        edit = True

        for db_item in db_items_per_user.values():
            block_storage_quota.remove(db_obj=db_item)
            edit = True
        for db_item in db_items_total.values():
            block_storage_quota.remove(db_obj=db_item)
            edit = True

        return edit


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
    """Compute Service Create, Read, Update and Delete operations."""

    def create(
        self,
        *,
        obj_in: ComputeServiceCreateExtended,
        region: Region,
        projects: List[Project] = None,
    ) -> ComputeService:
        """Create a new Block Storage Service.

        Connect the service to the given region and create all relative flavors, images
        and quotas. Filter projects based on received ones and target one. For quotas it
        must be exactly one.
        """
        if projects is None:
            projects = []
        db_obj = super().create(obj_in=obj_in)
        db_obj.region.connect(region)
        for item in obj_in.flavors:
            db_projects = list(filter(lambda x: x.uuid in item.projects, projects))
            flavor.create(obj_in=item, service=db_obj, projects=db_projects)
        for item in obj_in.images:
            db_projects = list(filter(lambda x: x.uuid in item.projects, projects))
            image.create(obj_in=item, service=db_obj, projects=db_projects)
        for item in obj_in.quotas:
            db_projects = list(filter(lambda x: x.uuid == item.project, projects))
            if len(db_projects) == 1:
                compute_quota.create(
                    obj_in=item, service=db_obj, project=db_projects[0]
                )
        return db_obj

    def remove(self, *, db_obj: ComputeService) -> bool:
        """Delete an existing service and all its relationships.

        At first delete its quotas. Then delete the flavors and images connected only to
        this service. Finally delete the service.
        """
        for item in db_obj.quotas:
            compute_quota.remove(db_obj=item)
        for item in db_obj.flavors:
            if len(item.services) == 1:
                flavor.remove(db_obj=item)
        for item in db_obj.images:
            if len(item.services) == 1:
                image.remove(db_obj=item)
        result = super().remove(db_obj=db_obj)
        return result

    def update(
        self,
        *,
        db_obj: ComputeService,
        obj_in: Union[ComputeServiceCreateExtended, ComputeServiceUpdate],
        projects: List[Project] = None,
        force: bool = False,
    ) -> Optional[ComputeService]:
        """Update Compute Service attributes.

        By default do not update relationships or default values. If force is True,
        update linked flavors, images, quotas and apply default values when explicit.
        """
        if projects is None:
            projects = []
        edit = False
        if force:
            flavors_updated = self.__update_flavors(
                db_obj=db_obj, obj_in=obj_in, provider_projects=projects
            )
            images_updated = self.__update_images(
                db_obj=db_obj, obj_in=obj_in, provider_projects=projects
            )
            quotas_updated = self.__update_quotas(
                db_obj=db_obj, obj_in=obj_in, provider_projects=projects
            )
            edit = flavors_updated or images_updated or quotas_updated

        if isinstance(obj_in, ComputeServiceCreateExtended):
            obj_in = ComputeServiceUpdate.parse_obj(obj_in)

        updated_data = super().update(db_obj=db_obj, obj_in=obj_in, force=force)
        return db_obj if edit else updated_data

    def __update_flavors(
        self,
        *,
        db_obj: ComputeService,
        obj_in: ComputeServiceCreateExtended,
        provider_projects: List[Project],
    ) -> bool:
        """Update service linked flavors.

        Connect new flavors not already connect, leave untouched already linked ones and
        delete old ones no more connected to the service.
        """
        edit = False
        db_items = {db_item.uuid: db_item for db_item in db_obj.flavors}
        for item in obj_in.flavors:
            db_item = db_items.pop(item.uuid, None)
            db_projects = list(
                filter(lambda x: x.uuid in item.projects, provider_projects)
            )
            if not db_item:
                flavor.create(obj_in=item, service=db_obj, projects=db_projects)
                edit = True
            else:
                updated_data = flavor.update(
                    db_obj=db_item, obj_in=item, projects=db_projects
                )
                if not edit and updated_data is not None:
                    edit = True
        for db_item in db_items.values():
            if len(db_item.services) == 1:
                flavor.remove(db_obj=db_item)
            else:
                db_obj.flavors.disconnect(db_item)
            edit = True
        return edit

    def __update_images(
        self,
        *,
        db_obj: ComputeService,
        obj_in: ComputeServiceCreateExtended,
        provider_projects: List[Project],
    ) -> bool:
        """Update service linked images.

        Connect new images not already connect, leave untouched already linked ones and
        delete old ones no more connected to the service.
        """
        edit = False
        db_items = {db_item.uuid: db_item for db_item in db_obj.images}
        for item in obj_in.images:
            db_item = db_items.pop(item.uuid, None)
            db_projects = list(
                filter(lambda x: x.uuid in item.projects, provider_projects)
            )
            if not db_item:
                image.create(obj_in=item, service=db_obj, projects=db_projects)
                edit = True
            else:
                updated_data = image.update(
                    db_obj=db_item, obj_in=item, projects=db_projects
                )
                if not edit and updated_data is not None:
                    edit = True
        for db_item in db_items.values():
            if len(db_item.services) == 1:
                image.remove(db_obj=db_item)
            else:
                db_obj.images.disconnect(db_item)
            edit = True
        return edit

    def __update_quotas(
        self,
        *,
        db_obj: ComputeService,
        obj_in: ComputeServiceCreateExtended,
        provider_projects: List[Project],
    ) -> bool:
        """Update service linked quotas.

        Connect new quotas not already connect, leave untouched already linked ones and
        delete old ones no more connected to the service.

        Split quotas in per_user and total. For each one of them, check the linked
        project. If the project already has a quota of that type, update that quota with
        the new received values.
        """
        edit = False

        db_items_per_user = {
            db_item.project.single().uuid: db_item
            for db_item in filter(lambda x: x.per_user, db_obj.quotas)
        }
        db_items_total = {
            db_item.project.single().uuid: db_item
            for db_item in filter(lambda x: not x.per_user, db_obj.quotas)
        }
        db_projects = {db_item.uuid: db_item for db_item in provider_projects}

        for item in obj_in.quotas:
            if item.per_user:
                db_item = db_items_per_user.pop(item.project, None)
                if not db_item:
                    compute_quota.create(
                        obj_in=item,
                        service=db_obj,
                        project=db_projects.get(item.project),
                    )
                    edit = True
                else:
                    updated_data = compute_quota.update(
                        db_obj=db_item,
                        obj_in=item,
                        projects=provider_projects,
                        force=True,
                    )
                    if not edit and updated_data is not None:
                        edit = True
            else:
                db_item = db_items_total.pop(item.project, None)
                if not db_item:
                    compute_quota.create(
                        obj_in=item,
                        service=db_obj,
                        project=db_projects.get(item.project),
                    )
                    edit = True
                else:
                    updated_data = compute_quota.update(
                        db_obj=db_item,
                        obj_in=item,
                        projects=provider_projects,
                        force=True,
                    )
                    if not edit and updated_data is not None:
                        edit = True

        for db_item in db_items_per_user.values():
            compute_quota.remove(db_obj=db_item)
            edit = True
        for db_item in db_items_total.values():
            compute_quota.remove(db_obj=db_item)
            edit = True

        return edit


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
    """Identity Service Create, Read, Update and Delete operations."""

    def create(
        self, *, obj_in: IdentityServiceCreate, region: Region
    ) -> IdentityService:
        """Create a new Block Storage Service.

        Connect the service to the given region.
        """
        db_obj = super().create(obj_in=obj_in)
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
    """Network Service Create, Read, Update and Delete operations."""

    def create(
        self,
        *,
        obj_in: NetworkServiceCreateExtended,
        region: Region,
        projects: List[Project] = None,
    ) -> NetworkService:
        """Create a new Block Storage Service.

        Connect the service to the given region and create all relative networks. Filter
        projects based on received ones and target one. It must be exactly one.
        """
        if projects is None:
            projects = []
        db_obj = super().create(obj_in=obj_in)
        db_obj.region.connect(region)
        for item in obj_in.networks:
            db_projects = list(filter(lambda x: x.uuid == item.project, projects))
            db_project = None
            if len(db_projects) == 1:
                db_project = db_projects[0]
            network.create(obj_in=item, service=db_obj, project=db_project)
        return db_obj

    def remove(self, *, db_obj: NetworkService) -> bool:
        """Delete an existing service and all its relationships.

        At first delete its quotas. Then delete the flavors and images connected only to
        this service. Finally delete the service.
        """
        for item in db_obj.networks:
            network.remove(db_obj=item)
        result = super().remove(db_obj=db_obj)
        return result

    def update(
        self,
        *,
        db_obj: NetworkService,
        obj_in: Union[NetworkServiceCreateExtended, NetworkServiceUpdate],
        projects: List[Project] = None,
        force: bool = False,
    ) -> Optional[NetworkService]:
        """Update Network Service attributes.

        By default do not update relationships or default values. If force is True,
        update linked networks and apply default values when explicit.
        """
        if projects is None:
            projects = []
        edit = False
        if force:
            edit = self.__update_networks(
                db_obj=db_obj, obj_in=obj_in, provider_projects=projects
            )

        if isinstance(obj_in, NetworkServiceCreateExtended):
            obj_in = NetworkServiceUpdate.parse_obj(obj_in)

        updated_data = super().update(db_obj=db_obj, obj_in=obj_in, force=force)
        return db_obj if edit else updated_data

    def __update_networks(
        self,
        *,
        db_obj: NetworkService,
        obj_in: NetworkServiceCreateExtended,
        provider_projects: List[Project],
    ) -> bool:
        """Update service linked networks.

        Connect new networks not already connect, leave untouched already linked ones
        and delete old ones no more connected to the service.
        """
        edit = False
        db_items = {db_item.uuid: db_item for db_item in db_obj.networks}
        for item in obj_in.networks:
            db_item = db_items.pop(item.uuid, None)
            db_projects = list(
                filter(lambda x: x.uuid == item.project, provider_projects)
            )
            if not db_item:
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
        return edit


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
