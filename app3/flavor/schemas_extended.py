from ..available_vm_flavor.schemas import (
    AvailableVMFlavor,
    AvailableVMFlavorCreate,
)
from ..flavor.schemas import Flavor, FlavorCreate

class FlavorCreateExtended(FlavorCreate):
    relationship: AvailableVMFlavorCreate


class FlavorExtended(Flavor):
    relationship: AvailableVMFlavor
