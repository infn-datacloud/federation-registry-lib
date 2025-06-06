"""Neomodel model of the User Group owned by an Identity Provider."""

from neomodel import (
    One,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)


class UserGroup(StructuredNode):
    """User Group owned by an Identity Provider.

    A User Group has a name which could not be unique
    (different Identity Providers can have same user group names).
    A User Group can be involved into multiple SLAs.
    A UserGroup has access, through its SLAs and Projects to a set of
    images, flavors, networks and quotas.

    Attributes:
    ----------
        id (int): User Group unique ID.
        description (str): Brief description.
        name (str): User Group name.
    """

    id = UniqueIdProperty()
    description = StringProperty(default="")
    name = StringProperty(required=True)

    projects = RelationshipTo(
        "fedreg.project.models.Project", "HAS_ACCESS_TO", cardinality=ZeroOrMore
    )
    identity_provider = RelationshipTo(
        "fedreg.identity_provider.models.IdentityProvider",
        "BELONGS_TO",
        cardinality=One,
    )
