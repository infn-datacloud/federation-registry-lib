from typing import List, Optional, Union

from app.crud import CRUDBase
from app.network.models import Network
from app.network.schemas import (
    NetworkCreate,
    NetworkRead,
    NetworkReadPublic,
    NetworkReadShort,
    NetworkUpdate,
)
from app.network.schemas_extended import NetworkReadExtended, NetworkReadExtendedPublic
from app.project.models import Project
from app.provider.schemas_extended import NetworkCreateExtended
from app.service.models import NetworkService


class CRUDNetwork(
    CRUDBase[
        Network,
        NetworkCreate,
        NetworkUpdate,
        NetworkRead,
        NetworkReadPublic,
        NetworkReadShort,
        NetworkReadExtended,
        NetworkReadExtendedPublic,
    ]
):
    """"""

    def create(
        self,
        *,
        obj_in: NetworkCreate,
        service: NetworkService,
        project: Optional[Project] = None
    ) -> Network:
        db_obj = super().create(obj_in=obj_in, force=True)
        db_obj.services.connect(service)
        if project is not None:
            db_obj.project.connect(project)
        return db_obj

    def update(
        self,
        *,
        db_obj: Network,
        obj_in: Union[NetworkUpdate, NetworkCreateExtended],
        projects: List[Project] = [],
        force: bool = False
    ) -> Optional[Network]:
        edit = False
        if force:
            db_projects = {db_item.uuid: db_item for db_item in projects}
            db_proj = db_obj.project.single()
            if obj_in.project is None and db_proj is not None:
                db_obj.project.disconnect(db_proj)
                edit = True
            elif db_proj is None or obj_in.project != db_proj.uuid:
                db_item = db_projects.get(obj_in.project)
                db_obj.project.replace(db_item)
                edit = True

        if isinstance(obj_in, NetworkCreateExtended):
            obj_in = NetworkUpdate.parse_obj(obj_in)

        updated_data = super().update(db_obj=db_obj, obj_in=obj_in, force=force)
        return db_obj if edit else updated_data


network = CRUDNetwork(
    model=Network,
    create_schema=NetworkCreate,
    read_schema=NetworkRead,
    read_public_schema=NetworkReadPublic,
    read_short_schema=NetworkReadShort,
    read_extended_schema=NetworkReadExtended,
    read_extended_public_schema=NetworkReadExtendedPublic,
)
