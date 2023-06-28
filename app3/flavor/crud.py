from .models import Flavor as FlavorModel
from .schemas import FlavorCreate, FlavorPatch
from ..crud import CRUDBase


class CRUDFlavor(CRUDBase[FlavorModel, FlavorCreate, FlavorPatch]):
    """"""


flavor = CRUDFlavor(FlavorModel, FlavorCreate)
