"""Neomodel model of the Virtual Machine Flavor owned by a Provider."""

from neomodel import (
    BooleanProperty,
    One,
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)


class StorageClass(StructuredNode):
    """Represent a storage class entity for kubernetes clusters.

    Attributes:
    ----------
        uid (str): Flavor unique ID.
        description (str): Brief description.
        name (str): Flavor name in the Resource Provider.
        provisioner (str): A provisioner determines what volume plugin is used for
            provisioning PVs
        is_default (bool): this storageclass is marked as the default one.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    name = StringProperty(required=True)
    provisioner = StringProperty(required=True)
    is_default = BooleanProperty(default=False)

    service = RelationshipFrom(
        "fedreg.service.models.BlockStorageService",
        "AVAILABLE_STORAGECLASS",
        cardinality=One,
    )
