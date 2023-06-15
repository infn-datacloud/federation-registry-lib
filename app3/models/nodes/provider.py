from neomodel import (
    ArrayProperty,
    BooleanProperty,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
    ZeroOrOne,
)
from ..relationships import (
    Project,
    AuthMethod,
    AvailableCluster,
    AvailableVMFlavor,
    AvailableVMImage,
    ProvideService,
)


class Provider(StructuredNode):
    """Provider class.

    A Provider has a list of maintainers, can be public
    and has a geographical localization. It support a set
    of images and flavors. It is involved in a set of SLA
    allowing user groups to access its own resources.

    Attributes:
        uid (int): Provider unique ID.
        name (str): Provider name (type).
        description (str): Brief description.
        support_email (list of str): List of maintainers emails.
        is_public (bool): Public or private provider.
    """

    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty(default="")
    is_public = BooleanProperty(default=False)
    support_email = ArrayProperty(StringProperty())

    slas = RelationshipFrom(
        ".SLA",
        "ACCESS_PROVIDER_THROUGH_PROJECT",
        cardinality=ZeroOrMore,
        model=Project,
    )
    services = RelationshipFrom(
        ".Service",
        "PROVIDES_SERVICE",
        cardinality=ZeroOrMore,
        model=ProvideService,
    )
    location = RelationshipTo(".Location", "LOCATED_AT", cardinality=ZeroOrOne)
    identity_providers = RelationshipTo(
        ".IdentityProvider",
        "ALLOW_AUTH_THROUGH",
        cardinality=ZeroOrMore,
        model=AuthMethod,
    )
    clusters = RelationshipTo(
        ".Cluster",
        "AVAILABLE_CLUSTER",
        cardinality=ZeroOrMore,
        model=AvailableCluster,
    )
    flavors = RelationshipTo(
        ".Flavor",
        "AVAILABLE_VM_SIZE",
        cardinality=ZeroOrMore,
        model=AvailableVMFlavor,
    )
    images = RelationshipTo(
        ".Image",
        "AVAILABLE_VM_IMAGE",
        cardinality=ZeroOrMore,
        model=AvailableVMImage,
    )
