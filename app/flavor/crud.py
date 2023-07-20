from app.crud import CRUDBase
from app.flavor.models import Flavor
from app.flavor.schemas import FlavorCreate, FlavorUpdate


class CRUDFlavor(CRUDBase[Flavor, FlavorCreate, FlavorUpdate]):
    """"""


flavor = CRUDFlavor(Flavor, FlavorCreate)
