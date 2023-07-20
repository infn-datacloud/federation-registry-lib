from app.crud import CRUDBase
from app.flavor.models import Flavor
from app.flavor.schemas import FlavorCreate, FlavorUpdate
from app.provider.models import Provider


class CRUDFlavor(CRUDBase[Flavor, FlavorCreate, FlavorUpdate]):
    """"""

    def create(
        self, *, obj_in: FlavorCreate, provider: Provider, force: bool = False
    ) -> Flavor:
        db_obj = super().create(obj_in=obj_in, force=force)
        db_obj.provider.connect(provider)
        return db_obj


flavor = CRUDFlavor(Flavor, FlavorCreate)
