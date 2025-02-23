"""Neomodel model of the (Provider - Identity Provider) relationship."""

from neomodel import StringProperty, StructuredRel


class AuthMethod(StructuredRel):
    """Relationship linking a Provider with an Identity Provider.

    Attributes:
    ----------
        idp_name (str): Identity Provider name saved in the Resource Provider.
        protocol (str): Protocol to use when authenticating on this identity provider.
    """

    idp_name = StringProperty(required=True)
    protocol = StringProperty(required=True)
