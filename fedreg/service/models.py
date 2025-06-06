"""Neomodel models of the Service supplied by a Provider on a specific Region."""

from neomodel import (
    One,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)

from fedreg.service.enum import ServiceType


class Service(StructuredNode):
    """Service supplied by a Provider on a specific Region.

    Common attributes to all service types.
    Any service is accessible through an endpoint, which is unique in the DB.

    Attributes:
    ----------
        id (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
    """

    id = UniqueIdProperty()
    description = StringProperty(default="")
    endpoint = StringProperty(required=True)
    name = StringProperty(required=True)
    type = StringProperty(required=True)

    region = RelationshipFrom(
        "fedreg.region.models.Region", "SUPPLIES", cardinality=One
    )


class BlockStorageService(Service):
    """Service managing Block Storage resources.

    A Block Storage Service, for each project, support a set of quotas managing the
    block storage resources.

    Attributes:
    ----------
        id (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
    """

    type = StringProperty(default=ServiceType.BLOCK_STORAGE.value)

    quotas = RelationshipFrom(
        "fedreg.quota.models.BlockStorageQuota", "APPLIES_TO", cardinality=ZeroOrMore
    )

    def pre_delete(self):
        """Remove related quotas."""
        for item in self.quotas:
            item.delete()


class ComputeService(Service):
    """Service managing Compute resources.

    A Compute Service, for each project, support a set of quotas managing the block
    storage resources. A Compute Service provides public and private Flavors and Images.

    Attributes:
    ----------
        id (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
    """

    type = StringProperty(default=ServiceType.COMPUTE.value)

    flavors = RelationshipTo(
        "fedreg.flavor.models.Flavor",
        "AVAILABLE_VM_FLAVOR",
        cardinality=ZeroOrMore,
    )
    images = RelationshipTo(
        "fedreg.image.models.Image",
        "AVAILABLE_VM_IMAGE",
        cardinality=ZeroOrMore,
    )
    quotas = RelationshipFrom(
        "fedreg.quota.models.ComputeQuota", "APPLIES_TO", cardinality=ZeroOrMore
    )

    def pre_delete(self):
        """Remove related quotas, flavors and images.

        Remove Flavors and Images only when this service is the only one using them.
        """
        for item in self.quotas:
            item.delete()
        for item in self.flavors:
            item.delete()
        for item in self.images:
            if len(item.services) == 1:
                item.delete()


class NetworkService(Service):
    """Service managing Network resources.

    A Network Service provides public and private Networks.

    Attributes:
    ----------
        id (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
    """

    type = StringProperty(default=ServiceType.NETWORKING.value)

    networks = RelationshipTo(
        "fedreg.network.models.Network",
        "AVAILABLE_NETWORK",
        cardinality=ZeroOrMore,
    )
    quotas = RelationshipFrom(
        "fedreg.quota.models.NetworkQuota", "APPLIES_TO", cardinality=ZeroOrMore
    )

    def pre_delete(self):
        """Remove related quotas and networks."""
        for item in self.quotas:
            item.delete()
        for item in self.networks:
            item.delete()


class ObjectStoreService(Service):
    """Service managing Object Storage resources.

    An Object Storage Service, for each project, support a set of quotas managing the
    object storage resources.

    Attributes:
    ----------
        id (int): Service unique ID.
        description (str): Brief description.
        endpoint (str): URL of the IaaS Service.
        type (str): Service type.
        name (str): Service name.
    """

    type = StringProperty(default=ServiceType.OBJECT_STORE.value)

    quotas = RelationshipFrom(
        "fedreg.quota.models.ObjectStoreQuota", "APPLIES_TO", cardinality=ZeroOrMore
    )

    def pre_delete(self):
        """Remove related quotas."""
        for item in self.quotas:
            item.delete()
