from neomodel import StringProperty, StructuredRel


class AvailableVMFlavor(StructuredRel):
    """Relationship linking a VM Flavor to a Provider.

    Attributes:
        name (str): Name of the Flavor in the Provider.
        uuid (uuid): Flavor Unique ID in the Provider.
    """

    name = StringProperty(required=True)
    uuid = StringProperty(required=True)
