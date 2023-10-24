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


class Region(StructuredNode):
    """Region owned by a Provider.

    A Region is used to split a provider resources and limit projects access.
    A Region can have a specific geographical location and supplies
    different services (compute, block storage, network...).

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
        "..provider.models.Provider", "DIVIDED_INTO", cardinality=One
    )
    services = RelationshipTo(
        "..service.models.Service", "SUPPLY", cardinality=ZeroOrMore
    )
