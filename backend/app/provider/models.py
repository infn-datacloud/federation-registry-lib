from app.auth_method.models import AuthMethod
from neomodel import (
    ArrayProperty,
    BooleanProperty,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)


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
    name = StringProperty(required=True)
    type = StringProperty(required=True)
    status = StringProperty()
    is_public = BooleanProperty(default=False)
    support_emails = ArrayProperty(StringProperty())

    projects = RelationshipTo(
        "..project.models.Project",
        "BOOK_PROJECT_FOR_SLA",
        cardinality=ZeroOrMore,
    )
    regions = RelationshipTo(
        "..region.models.Region", "DIVIDED_INTO", cardinality=ZeroOrMore
    )
    identity_providers = RelationshipTo(
        "..identity_provider.models.IdentityProvider",
        "ALLOW_AUTH_THROUGH",
        cardinality=ZeroOrMore,
        model=AuthMethod,
    )
