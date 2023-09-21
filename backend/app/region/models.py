from neomodel import (
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
    ZeroOrOne,
)


class Region(StructuredNode):
    """Associated Region class.

    Relationship linking a user group to a provider.
    This link correspond to a "Region/tenant" entity.

    Attributes:
        uid (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    name = StringProperty(required=True)

    location = RelationshipTo(
        "..location.models.Location", "LOCATED_AT", cardinality=ZeroOrOne
    )
    provider = RelationshipFrom(
        "..provider.models.Provider", "DIVIDED_INTO", cardinality=ZeroOrOne
    )
    services = RelationshipTo(
        "..service.models.Service", "SUPPLY", cardinality=ZeroOrMore
    )
