"""Neomodel model Identity Provider."""
from neomodel import (
    OneOrMore,
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)

from fedreg.auth_method.models import AuthMethod


class IdentityProvider(StructuredNode):
    """Identity Provider.

    An Identity Provider is used to authenticate operations.
    It has multiple User Groups and can be used by multiple Providers.
    It is reachable at a specific endpoint and can be accessed
    by a set of services owned by an authorized Provider.

    Attributes:
    ----------
        uid (int): Identity Provider unique ID.
        description (str): Brief description.
        endpoint (str): URL of the Identity Provider.
        group_claim (str): value of the key from which retrieve
            the user group name from an authentication token.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    endpoint = StringProperty(unique_index=True, required=True)
    group_claim = StringProperty(required=True)

    providers = RelationshipFrom(
        "fedreg.provider.models.Provider",
        "ALLOW_AUTH_THROUGH",
        cardinality=OneOrMore,
        model=AuthMethod,
    )
    user_groups = RelationshipFrom(
        "fedreg.user_group.models.UserGroup",
        "BELONG_TO",
        cardinality=ZeroOrMore,
    )
