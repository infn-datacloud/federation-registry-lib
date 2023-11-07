from typing import List, Optional, Union

from app.crud import CRUDBase
from app.project.models import Project
from app.provider.schemas_extended import (
    BlockStorageQuotaCreateExtended,
    ComputeQuotaCreateExtended,
)
from app.quota.models import BlockStorageQuota, ComputeQuota
from app.quota.schemas import (
    BlockStorageQuotaCreate,
    BlockStorageQuotaRead,
    BlockStorageQuotaReadPublic,
    BlockStorageQuotaReadShort,
    BlockStorageQuotaUpdate,
    ComputeQuotaCreate,
    ComputeQuotaRead,
    ComputeQuotaReadPublic,
    ComputeQuotaReadShort,
    ComputeQuotaUpdate,
)
from app.quota.schemas_extended import (
    BlockStorageQuotaReadExtended,
    BlockStorageQuotaReadExtendedPublic,
    ComputeQuotaReadExtended,
    ComputeQuotaReadExtendedPublic,
)
from app.service.models import BlockStorageService, ComputeService


class CRUDBlockStorageQuota(
    CRUDBase[
        BlockStorageQuota,
        BlockStorageQuotaCreate,
        BlockStorageQuotaUpdate,
        BlockStorageQuotaRead,
        BlockStorageQuotaReadPublic,
        BlockStorageQuotaReadShort,
        BlockStorageQuotaReadExtended,
        BlockStorageQuotaReadExtendedPublic,
    ]
):
    """Block Storage Quota Create, Read, Update and Delete operations."""

    def create(
        self,
        *,
        obj_in: BlockStorageQuotaCreate,
        service: BlockStorageService,
        project: Project,
    ) -> BlockStorageQuota:
        """Create a new Block Storage Quota.

        Connect the quota to the given service and project.
        """
        db_obj = super().create(obj_in=obj_in)
        db_obj.service.connect(service)
        db_obj.project.connect(project)
        return db_obj

    def update(
        self,
        *,
        db_obj: BlockStorageQuota,
        obj_in: Union[BlockStorageQuotaCreateExtended, BlockStorageQuotaUpdate],
        projects: Optional[List[Project]] = None,
        force: bool = False,
    ) -> Optional[BlockStorageQuota]:
        """Update Quota attributes.

        By default do not update relationships or default values. If force is True, if
        different from the current one, replace linked project and apply default values
        when explicit.
        """
        if projects is None:
            projects = []
        edit = False
        if force:
            db_projects = {db_item.uuid: db_item for db_item in projects}
            db_proj = db_obj.project.single()
            if obj_in.project != db_proj.uuid:
                db_item = db_projects.get(obj_in.project)
                db_obj.project.reconnect(db_proj, db_item)
                edit = True

        if isinstance(obj_in, BlockStorageQuotaCreateExtended):
            obj_in = BlockStorageQuotaUpdate.parse_obj(obj_in)

        updated_data = super().update(db_obj=db_obj, obj_in=obj_in, force=force)
        return db_obj if edit else updated_data


class CRUDComputeQuota(
    CRUDBase[
        ComputeQuota,
        ComputeQuotaCreate,
        ComputeQuotaUpdate,
        ComputeQuotaRead,
        ComputeQuotaReadPublic,
        ComputeQuotaReadShort,
        ComputeQuotaReadExtended,
        ComputeQuotaReadExtendedPublic,
    ]
):
    """Compute Quota Create, Read, Update and Delete operations."""

    def create(
        self,
        *,
        obj_in: ComputeQuotaCreate,
        service: ComputeService,
        project: Project,
    ) -> ComputeQuota:
        """Create a new Compute Quota.

        Connect the quota to the given service and project.
        """
        db_obj = super().create(obj_in=obj_in)
        db_obj.service.connect(service)
        db_obj.project.connect(project)
        return db_obj

    def update(
        self,
        *,
        db_obj: ComputeQuota,
        obj_in: Union[ComputeQuotaCreateExtended, ComputeQuotaUpdate],
        projects: Optional[List[Project]] = None,
        force: bool = False,
    ) -> Optional[ComputeQuota]:
        """Update Quota attributes.

        By default do not update relationships or default values. If force is True, if
        different from the current one, replace linked project and apply default values
        when explicit.
        """
        if projects is None:
            projects = []
        edit = False
        if force:
            db_projects = {db_item.uuid: db_item for db_item in projects}
            db_proj = db_obj.project.single()
            if obj_in.project != db_proj.uuid:
                db_item = db_projects.get(obj_in.project)
                db_obj.project.reconnect(db_proj, db_item)
                edit = True

        if isinstance(obj_in, ComputeQuotaCreateExtended):
            obj_in = ComputeQuotaUpdate.parse_obj(obj_in)

        updated_data = super().update(db_obj=db_obj, obj_in=obj_in, force=force)
        return db_obj if edit else updated_data


block_storage_quota = CRUDBlockStorageQuota(
    model=BlockStorageQuota,
    create_schema=BlockStorageQuotaCreate,
    read_schema=BlockStorageQuotaRead,
    read_public_schema=BlockStorageQuotaReadPublic,
    read_short_schema=BlockStorageQuotaReadShort,
    read_extended_schema=BlockStorageQuotaReadExtended,
    read_extended_public_schema=BlockStorageQuotaReadExtendedPublic,
)
compute_quota = CRUDComputeQuota(
    model=ComputeQuota,
    create_schema=ComputeQuotaCreate,
    read_schema=ComputeQuotaRead,
    read_public_schema=ComputeQuotaReadPublic,
    read_short_schema=ComputeQuotaReadShort,
    read_extended_schema=ComputeQuotaReadExtended,
    read_extended_public_schema=ComputeQuotaReadExtendedPublic,
)
