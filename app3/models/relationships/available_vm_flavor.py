from neomodel import StringProperty, StructuredRel


class AvailableVMFlavor(StructuredRel):
    """Supported Flavor class.

    Relationship linking a flavor to the provider
    supporting it.

    Attributes:
        uid (uuid): SupportedFlavor unique ID.
        flavor_name (str): Name given to the Flavor
            by the Provider.
        flavor_id (uuid): Flavor Unique ID in the Provider.
    """

    name = StringProperty(required=True)
    uuid = StringProperty(required=True)
