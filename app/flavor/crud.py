from app.flavor.models import Flavor
from app.flavor.schemas import FlavorCreate, FlavorUpdate
from app.crud import CRUDBase


class CRUDFlavor(CRUDBase[Flavor, FlavorCreate, FlavorUpdate]):
    """"""


flavor = CRUDFlavor(Flavor, FlavorCreate)
