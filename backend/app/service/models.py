from neomodel import (
    One,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)


class Service(StructuredNode):
    """Service class.

    A Service manages a specific amount of resource types
    defined by a set of quotas and belonging to an SLA.
    It is accessible through an endpoint.

    TODO: Authentication
    through IAM can be accepted. It can accept multiple
    authentication methods. It can be public or private.

    Attributes:
        uid (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    endpoint = StringProperty(unique_index=True, required=True)
    type = StringProperty(required=True)
    name = StringProperty(required=True)

    region = RelationshipFrom("..region.models.Region", "SUPPLY", cardinality=One)


class ComputeService(Service):
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
    quotas = RelationshipFrom(
        "..quota.models.ComputeQuota", "APPLY_TO", cardinality=ZeroOrMore
    )


class BlockStorageService(Service):
    quotas = RelationshipFrom(
        "..quota.models.BlockStorageQuota", "APPLY_TO", cardinality=ZeroOrMore
    )


class KeystoneService(Service):
    pass
