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
from ..auth_method.models import AuthMethod
from ..available_cluster.models import AvailableCluster
from ..available_vm_flavor.models import AvailableVMFlavor
from ..available_vm_image.models import AvailableVMImage
from ..book_project.models import BookProject


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

    projects = RelationshipTo(
        "..project.models.Project",
        "BOOK_PROJECT_FOR_AN_SLA",
        cardinality=ZeroOrMore,
        model=BookProject,
    )
    services = RelationshipFrom(
        "..service.models.Service", "PROVIDES_SERVICE", cardinality=ZeroOrMore
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
    clusters = RelationshipTo(
        "..cluster.models.Cluster",
        "AVAILABLE_CLUSTER",
        cardinality=ZeroOrMore,
        model=AvailableCluster,
    )
    flavors = RelationshipTo(
        "..flavor.models.Flavor",
        "AVAILABLE_VM_SIZE",
        cardinality=ZeroOrMore,
        model=AvailableVMFlavor,
    )
    images = RelationshipTo(
        "..image.models.Image",
        "AVAILABLE_VM_IMAGE",
        cardinality=ZeroOrMore,
        model=AvailableVMImage,
    )
