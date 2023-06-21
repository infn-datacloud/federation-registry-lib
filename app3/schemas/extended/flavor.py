from ..nodes.flavor import Flavor, FlavorCreate
from ..relationships.available_vm_flavor import AvailableVMFlavor, AvailableVMFlavorCreate


class FlavorCreateExtended(FlavorCreate):
    relationship: AvailableVMFlavorCreate


class FlavorExtended(Flavor):
    relationship: AvailableVMFlavor
