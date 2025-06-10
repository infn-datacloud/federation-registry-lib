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

from fedreg.v2.network.models import IsDefault


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
        uid (uuid): AssociatedProject unique ID.
        description (str): Brief description.
        name (str): Name of the project in the Provider.
        uuid (uuid): Project Unique ID in the Provider.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    name = StringProperty(required=True)
    uuid = StringProperty(required=True)

    provider = RelationshipFrom(
        "fedreg.v2.provider.models.Provider",
        "BOOKS_PROJECT",
        cardinality=One,
    )
    user_group = RelationshipFrom(
        "fedreg.v2.user_group.models.UserGroup",
        "HAS_ACCESS_TO",
        cardinality=ZeroOrOne,
    )
    quotas = RelationshipTo(
        "fedreg.v2.quota.models.Quota",
        "HAS_USAGE_LIMITS",
        cardinality=ZeroOrMore,
    )
    flavors = RelationshipTo(
        "fedreg.v2.flavor.models.Flavor",
        "CAN_USE_VM_FLAVOR",
        cardinality=ZeroOrMore,
    )
    images = RelationshipTo(
        "fedreg.v2.image.models.Image",
        "CAN_USE_VM_IMAGE",
        cardinality=ZeroOrMore,
    )
    networks = RelationshipTo(
        "fedreg.v2.network.models.Network",
        "CAN_USE_NETWORK",
        cardinality=ZeroOrMore,
        model=IsDefault,
    )

    def pre_delete(self):
        """Remove related quotas and SLA.

        Remove the SLA only if that SLA points only to this project.
        """
        for item in self.quotas:
            item.delete()
