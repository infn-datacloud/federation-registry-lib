from app.flavor.models import Flavor as FlavorModel
from app.flavor.schemas import FlavorCreate, FlavorUpdate
from app.crud import CRUDBase


class CRUDFlavor(CRUDBase[FlavorModel, FlavorCreate, FlavorUpdate]):
    """"""


flavor = CRUDFlavor(FlavorModel, FlavorCreate)
