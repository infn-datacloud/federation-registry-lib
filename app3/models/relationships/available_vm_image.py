from neomodel import StringProperty, StructuredRel


class AvailableVMImage(StructuredRel):
    """Supported Image class.

    Relationship linking a flavor to the provider
    supporting it.

    Attributes:
        uid (uuid): SupportedImage unique ID.
        flavor_name (str): Name given to the Image
            by the Provider.
        flavor_id (uuid): Image Unique ID in the Provider.
    """

    name = StringProperty(required=True)
    uuid = StringProperty(required=True)
