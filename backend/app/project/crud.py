from app.crud import CRUDBase
from app.project.models import Project
from app.project.schemas import (
    ProjectCreate,
    ProjectRead,
    ProjectReadPublic,
    ProjectReadShort,
    ProjectUpdate,
)
from app.project.schemas_extended import ProjectReadExtended, ProjectReadExtendedPublic
from app.provider.models import Provider
from app.quota.crud import block_storage_quota, compute_quota
from app.quota.models import BlockStorageQuota, ComputeQuota
from app.sla.crud import sla


class CRUDProject(
    CRUDBase[
        Project,
        ProjectCreate,
        ProjectUpdate,
        ProjectRead,
        ProjectReadPublic,
        ProjectReadShort,
        ProjectReadExtended,
        ProjectReadExtendedPublic,
    ]
):
    """Flavor Create, Read, Update and Delete operations."""

    def create(self, *, obj_in: ProjectCreate, provider: Provider) -> Project:
        """Create a new Project.

        Connect the project to the given provider.
        """
        db_obj = super().create(obj_in=obj_in)
        db_obj.provider.connect(provider)
        return db_obj

    def remove(self, *, db_obj: Project) -> bool:
        """Delete an existing project and all its relationships.

        At first delete its quotas. Then, if the linked SLA points only
        to this project, delete it. Otherwise do nothing. Finally delete
        the project.
        """
        for item in db_obj.quotas:
            if isinstance(item, BlockStorageQuota):
                block_storage_quota.remove(db_obj=item)
            elif isinstance(item, ComputeQuota):
                compute_quota.remove(db_obj=item)
        item = db_obj.sla.single()
        if item and len(item.projects) == 1:
            sla.remove(db_obj=item)
        return super().remove(db_obj=db_obj)


project = CRUDProject(
    model=Project,
    create_schema=ProjectCreate,
    read_schema=ProjectRead,
    read_public_schema=ProjectReadPublic,
    read_short_schema=ProjectReadShort,
    read_extended_schema=ProjectReadExtended,
    read_extended_public_schema=ProjectReadExtendedPublic,
)
