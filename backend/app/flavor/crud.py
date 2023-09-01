from app.crud import CRUDBase
from app.flavor.models import Flavor
from app.flavor.schemas import (
    FlavorCreate,
    FlavorRead,
    FlavorReadPublic,
    FlavorReadShort,
    FlavorUpdate,
)
from app.flavor.schemas_extended import FlavorReadExtended, FlavorReadExtendedPublic
from app.provider.models import Provider


class CRUDFlavor(
    CRUDBase[
        Flavor,
        FlavorCreate,
        FlavorUpdate,
        FlavorRead,
        FlavorReadPublic,
        FlavorReadShort,
        FlavorReadExtended,
        FlavorReadExtendedPublic,
    ]
):
    """"""

    def create(
        self, *, obj_in: FlavorCreate, provider: Provider, force: bool = False
    ) -> Flavor:
        db_obj = super().create(obj_in=obj_in, force=force)
        db_obj.provider.connect(provider)
        return db_obj


flavor = CRUDFlavor(
    model=Flavor,
    create_schema=FlavorCreate,
    read_schema=FlavorRead,
    read_public_schema=FlavorReadPublic,
    read_short_schema=FlavorReadShort,
    read_extended_schema=FlavorReadExtended,
    read_extended_public_schema=FlavorReadExtendedPublic,
)
