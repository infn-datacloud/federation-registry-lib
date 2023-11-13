from typing import List, Optional, Union

from app.crud import CRUDBase
from app.project.models import Project
from app.provider.schemas_extended import SLACreateExtended
from app.sla.models import SLA
from app.sla.schemas import (
    SLACreate,
    SLARead,
    SLAReadPublic,
    SLAReadShort,
    SLAUpdate,
)
from app.sla.schemas_extended import SLAReadExtended, SLAReadExtendedPublic
from app.user_group.models import UserGroup


class CRUDSLA(
    CRUDBase[
        SLA,
        SLACreate,
        SLAUpdate,
        SLARead,
        SLAReadPublic,
        SLAReadShort,
        SLAReadExtended,
        SLAReadExtendedPublic,
    ]
):
    """SLA Create, Read, Update and Delete operations."""

    def create(
        self, *, obj_in: SLACreate, project: Project, user_group: UserGroup
    ) -> SLA:
        """Create a new SLA.

        At first check an SLA pointing to the same document does not exist yet. If it
        does not exist, create it. In any case connect the SLA to the given user group
        and project. If the project already has an attached SLA, disconnect it.
        """
        db_obj = user_group.slas.get_or_none(doc_uuid=obj_in.doc_uuid)
        if not db_obj:
            db_obj = super().create(obj_in=obj_in)
            db_obj.user_group.connect(user_group)
        old_sla = project.sla.single()
        if old_sla:
            project.sla.disconnect(old_sla)
        db_obj.projects.connect(project)
        return db_obj

    def update(
        self,
        *,
        db_obj: SLA,
        obj_in: Union[SLAUpdate, SLACreateExtended],
        projects: Optional[List[Project]] = None,
        force: bool = False,
    ) -> Optional[SLA]:
        """Update SLA attributes.

        By default do not update relationships or default values. If force is True,
        update linked projects and apply default values when explicit.

        To update projects, since the forced update happens when creating or updating a
        provider, we filter all the existing projects on this provider already connected
        to this SLA, should be just one. If there is a project already connected we
        replace the old one with the new one, otherwise we immediately connect the new
        one.
        """
        if projects is None:
            projects = []
        edit = False
        if force:
            provider_projects = {db_item.uuid: db_item for db_item in projects}
            new_project = provider_projects.get(obj_in.project)
            old_project = next(filter(lambda x: x in db_obj.projects, projects), None)

            if not old_project:
                db_obj.projects.connect(new_project)
                edit = True
            elif old_project.uuid != obj_in.project:
                db_obj.projects.reconnect(old_project, new_project)
                edit = True

        if isinstance(obj_in, SLACreateExtended):
            obj_in = SLAUpdate.parse_obj(obj_in)

        updated_data = super().update(db_obj=db_obj, obj_in=obj_in, force=force)
        return db_obj if edit else updated_data


sla = CRUDSLA(
    model=SLA,
    create_schema=SLACreate,
    read_schema=SLARead,
    read_public_schema=SLAReadPublic,
    read_short_schema=SLAReadShort,
    read_extended_schema=SLAReadExtended,
    read_extended_public_schema=SLAReadExtendedPublic,
)
