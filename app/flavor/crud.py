from .models import Flavor as FlavorModel
from .schemas import FlavorCreate, FlavorUpdate
from ..crud import CRUDBase


class CRUDFlavor(CRUDBase[FlavorModel, FlavorCreate, FlavorUpdate]):
    """"""


flavor = CRUDFlavor(FlavorModel, FlavorCreate)
