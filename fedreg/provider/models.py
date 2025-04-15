"""Neomodel model of the Resource Provider (openstack, kubernetesapp..)."""

from neomodel import (
    ArrayProperty,
    BooleanProperty,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)

from fedreg.auth_method.models import AuthMethod
from fedreg.image.models import Image
from fedreg.provider.enum import ProviderStatus
from fedreg.service.enum import ServiceType


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
        status (str | None): Provider status.
        is_public (bool): Public or private Provider.
        support_email (list of str): list of maintainers emails.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    name = StringProperty(required=True)
    type = StringProperty(required=True)
    status = StringProperty(default=ProviderStatus.ACTIVE.value)
    is_public = BooleanProperty(default=False)
    support_emails = ArrayProperty(StringProperty(), default=[])

    projects = RelationshipTo(
        "fedreg.project.models.Project",
        "BOOK_PROJECT_FOR_SLA",
        cardinality=ZeroOrMore,
    )
    regions = RelationshipTo(
        "fedreg.region.models.Region", "DIVIDED_INTO", cardinality=ZeroOrMore
    )
    identity_providers = RelationshipTo(
        "fedreg.identity_provider.models.IdentityProvider",
        "ALLOW_AUTH_THROUGH",
        cardinality=ZeroOrMore,
        model=AuthMethod,
    )

    def images(self) -> list[Image]:
        """List provider's available images.

        Make a cypher query to retrieve all provider's images.
        """
        results, _ = self.cypher(
            f"""
                MATCH (p:Provider)
                WHERE (elementId(p)=$self)
                MATCH (p)-[:`DIVIDED_INTO`]-(r)
                MATCH (r)-[:`SUPPLY`]-(s)
                WHERE s.type = "{ServiceType.COMPUTE.value}"
                MATCH (s)-[:`AVAILABLE_VM_IMAGE`]->(i:Image)
                RETURN DISTINCT i
            """
        )
        return [Image.inflate(row[0]) for row in results]

    def pre_delete(self):
        """Delete related identity providers, projects and regions.

        Remove the identity ptovider only if that idp points only to this provider.
        """
        for item in self.projects:
            item.delete()
        for item in self.regions:
            item.delete()
