from neomodel import (
    StructuredNode,
    UniqueIdProperty,
    StringProperty,
    BooleanProperty,
    RelationshipFrom,
    ZeroOrMore,
)


class IdentityProvider(StructuredNode):
    """Provider Base class

    Class without id which is populated by the database.

    Attributes:
        name (str): Provider name.
        is_public (bool): Public Provider.
        slas (list of SLA): List of SLAs related to the Provider.
        # TODO: Country name, code and location can be grouped in
        a separate entity.
    """

    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    url = StringProperty(required=True)
    protocol = BooleanProperty(required=True)

    services = RelationshipFrom(
        ".Service", "AUTHENTICATE_THROUGH", cardinality=ZeroOrMore
    )
