"""Neomodel model of the Resource Provider (openstack, kubernetesapp..)."""

from neomodel import (
    BooleanProperty,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)

from fedreg.auth_method.models import AuthMethod


class Provider(StructuredNode):
    """Provider (openstack, kubernetesapp..).

    A Provider has a name which could not be unique, providers with
    same name must have different type; for example a site
    provides different providers with same name but one is an openstack instance
    the other is a kubernetes cluster.
    It has a list of maintainers, can be public or private.
    The provider status is used to notify users if the provider is available or not.
    It is divided into Regions (at least one).
    It allows authentication through multiple Identity Providers.
    It support multiple Projects.

    Attributes:
    ----------
        uid (int): Provider unique ID.
        description (str): Brief description.
        name (str): Provider name.
        type (str): Provider type.
        is_public (bool): Public or private Provider.
        connection_url (str): Connection URL of the Provider.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    name = StringProperty(required=True)
    type = StringProperty(required=True)
    is_public = BooleanProperty(default=False)
    connection_url = StringProperty(required=True)

    projects = RelationshipTo(
        "fedreg.project.models.Project",
        "BOOKS_PROJECT",
        cardinality=ZeroOrMore,
    )
    regions = RelationshipTo(
        "fedreg.region.models.Region", "DIVIDED_INTO", cardinality=ZeroOrMore
    )
    identity_providers = RelationshipTo(
        "fedreg.identity_provider.models.IdentityProvider",
        "ALLOWS_AUTH_THROUGH",
        cardinality=ZeroOrMore,
        model=AuthMethod,
    )

    def pre_delete(self):
        """Delete related projects and regions."""
        for item in self.projects:
            item.delete()
        for item in self.regions:
            item.delete()
