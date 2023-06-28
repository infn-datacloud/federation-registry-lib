from ..available_vm_flavor.schemas import (
    AvailableVMFlavor,
    AvailableVMFlavorCreate,
    AvailableVMFlavorUpdate,
)
from ..flavor.schemas import Flavor, FlavorCreate, FlavorUpdate


class FlavorCreateExtended(FlavorCreate):
    relationship: AvailableVMFlavorCreate


class FlavorUpdateExtended(FlavorUpdate):
    relationship: AvailableVMFlavorUpdate


class FlavorExtended(Flavor):
    relationship: AvailableVMFlavor
