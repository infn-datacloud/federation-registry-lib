from neomodel import (
    ArrayProperty,
    BooleanProperty,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
    ZeroOrOne,
)
from app.auth_method.models import AuthMethod


class Provider(StructuredNode):
    """Provider class.

    A Provider has a list of maintainers, can be public
    and has a geographical localization. It support a set
    of images and flavors. It is involved in a set of SLA
    allowing user groups to access its own resources.

    Attributes:
        uid (int): Provider unique ID.
        description (str): Brief description.
        name (str): Provider name (type).
        is_public (bool): Public or private provider.
        support_email (list of str): List of maintainers emails.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    name = StringProperty(unique_index=True, required=True)
    is_public = BooleanProperty(default=False)
    support_emails = ArrayProperty(StringProperty())

    projects = RelationshipTo(
        "..project.models.Project",
        "BOOK_PROJECT_FOR_SLA",
        cardinality=ZeroOrMore,
    )
    services = RelationshipTo(
        "..service.models.Service", "SUPPLY", cardinality=ZeroOrMore
    )
    location = RelationshipTo(
        "..location.models.Location", "LOCATED_AT", cardinality=ZeroOrOne
    )
    identity_providers = RelationshipTo(
        "..identity_provider.models.IdentityProvider",
        "ALLOW_AUTH_THROUGH",
        cardinality=ZeroOrMore,
        model=AuthMethod,
    )
    flavors = RelationshipTo(
        "..flavor.models.Flavor",
        "AVAILABLE_VM_FLAVOR",
        cardinality=ZeroOrMore,
    )
    images = RelationshipTo(
        "..image.models.Image",
        "AVAILABLE_VM_IMAGE",
        cardinality=ZeroOrMore,
    )
