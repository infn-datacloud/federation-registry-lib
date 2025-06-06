"""Neomodel model of the Project owned by a Provider."""

from neomodel import (
    One,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
    ZeroOrOne,
)


class Project(StructuredNode):
    """Project owned by a Provider.

    A project/tenant/namespace is uniquely identified in the
    Provider by its uuid.
    It has a name and can access all shared flavors, images
    and networks plus the private flavors, images and networks.
    It has a set of quotas limiting the resources it can use on
    a specific service of the hosting Provider.
    A project should always be pointed by an SLA.

    Attributes:
    ----------
        id (uuid): AssociatedProject unique ID.
        description (str): Brief description.
        name (str): Name of the project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
    """

    id = UniqueIdProperty()
    description = StringProperty(default="")
    name = StringProperty(required=True)
    uuid = StringProperty(required=True)

    provider = RelationshipFrom(
        "fedreg.provider.models.Provider",
        "BOOKS_PROJECT",
        cardinality=One,
    )
    user_group = RelationshipFrom(
        "fedreg.user_group.models.UserGroup",
        "HAS_ACCESS_TO",
        cardinality=ZeroOrOne,
    )
    quotas = RelationshipTo(
        "fedreg.quota.models.Quota",
        "HAS_USAGE_LIMITS",
        cardinality=ZeroOrMore,
    )
    usage = RelationshipTo(
        "fedreg.quota.models.Usage",
        "CURRENT_USAGE",
        cardinality=ZeroOrMore,
    )
    flavors = RelationshipTo(
        "fedreg.flavor.models.Flavor",
        "CAN_USE_VM_FLAVOR",
        cardinality=ZeroOrMore,
    )
    images = RelationshipTo(
        "fedreg.image.models.Image",
        "CAN_USE_VM_IMAGE",
        cardinality=ZeroOrMore,
    )
    networks = RelationshipTo(
        "fedreg.network.models.Network",
        "CAN_USE_NETWORK",
        cardinality=ZeroOrMore,
    )

    def pre_delete(self):
        """Remove related quotas and SLA.

        Remove the SLA only if that SLA points only to this project.
        """
        for item in self.quotas:
            item.delete()
        for item in self.usage:
            item.delete()
