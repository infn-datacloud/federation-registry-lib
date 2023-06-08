from neomodel import (
    BooleanProperty,
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    StructuredRel,
    UniqueIdProperty,
    ZeroOrMore,
)


class AuthenticationMethod(StructuredRel):
    """Authentication Method class.

    Relationship linking a service to an identity provider.

    Attributes:
        uid (uuid): AuthenticationMethod unique ID.
        idp_name (str): Name given to the IDP by the
            Provider hosting the service.
        protocol (uuid): Authentication protocol.
    """

    uid = UniqueIdProperty()
    idp_name = StringProperty(required=True)
    protocol = BooleanProperty(required=True)


class IdentityProvider(StructuredNode):
    """Identity Provider class.

    An identity provider is used to authenticate operations.
    It is reachable at a specific endpoint and can be accessed
    by a set of services.

    Attributes:
        uid (int): IdentityProvider unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IdentityProvider.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    endpoint = StringProperty(required=True)

    services = RelationshipFrom(
        ".Service",
        "AUTHENTICATES_THROUGH",
        cardinality=ZeroOrMore,
        model=AuthenticationMethod,
    )
