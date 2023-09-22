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
        self, *, obj_in: NetworkCreate, service: NetworkService, force: bool = False
    ) -> Network:
        db_obj = super().create(obj_in=obj_in, force=force)
        db_obj.services.connect(service)
        return db_obj


network = CRUDNetwork(
    model=Network,
    create_schema=NetworkCreate,
    read_schema=NetworkRead,
    read_public_schema=NetworkReadPublic,
    read_short_schema=NetworkReadShort,
    read_extended_schema=NetworkReadExtended,
    read_extended_public_schema=NetworkReadExtendedPublic,
)
