from app.auth_method.models import AuthMethod
from neomodel import (
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)


class IdentityProvider(StructuredNode):
    """Identity Provider class.

    An identity provider is used to authenticate operations.
    It is reachable at a specific endpoint and can be accessed
    by a set of services.

    Attributes:
        uid (int): IdentityProvider unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IdentityProvider.
        group_claim (str): value of the key from which retrieve
            the user group name from a authentication token.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    endpoint = StringProperty(unique_index=True, required=True)
    group_claim = StringProperty(required=True)

    providers = RelationshipFrom(
        "..provider.models.Provider",
        "ALLOW_AUTH_THROUGH",
        cardinality=ZeroOrMore,
        model=AuthMethod,
    )
    user_groups = RelationshipFrom(
        "..user_group.models.UserGroup",
        "BELONG_TO",
        cardinality=ZeroOrMore,
    )
