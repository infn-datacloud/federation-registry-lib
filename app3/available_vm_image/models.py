from neomodel import StringProperty, StructuredRel


class AvailableVMImage(StructuredRel):
    """Relationship linking a VM Image to a Provider.

    Attributes:
        name (str): Name of the Image in the Provider.
        uuid (uuid): Image Unique ID in the Provider.
    """

    name = StringProperty(required=True)
    uuid = StringProperty(required=True)
