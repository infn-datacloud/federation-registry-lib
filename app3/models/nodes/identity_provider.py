from neomodel import (
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)
from ..relationships import AuthMethod


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

    providers = RelationshipFrom(
        ".Provider",
        "ALLOW_AUTH_THROUGH",
        cardinality=ZeroOrMore,
        model=AuthMethod,
    )
