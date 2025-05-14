"""Neomodel model of the (Provider - Identity Provider) relationship."""

from neomodel import StringProperty, StructuredRel


class AuthMethod(StructuredRel):
    """Relationship linking a Provider with an Identity Provider.

    Attributes:
    ----------
        idp_name (str | None): Identity Provider name saved in the Resource Provider.
        protocol (str | None): Protocol to use when authenticating on this identity
            provider.
        aud (str | None): Audience to use when authenticating on this identity provider.
    """

    idp_name = StringProperty(default=None)
    protocol = StringProperty(default=None)
    aud = StringProperty(default=None)
