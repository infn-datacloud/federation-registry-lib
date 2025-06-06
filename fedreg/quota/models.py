"""Neomodel models of the resource limitations for Projects on Services."""

from neomodel import (
    BooleanProperty,
    IntegerProperty,
    One,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)

from fedreg.service.enum import ServiceType


class Quota(StructuredNode):
    """Resource limitations for Projects on Services.

    Common attributes to all quota types.
    Any quota belongs to a only a project.

    Attributes:
    ----------
        id (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
    """

    id = UniqueIdProperty()
    description = StringProperty(default="")
    type = StringProperty(required=True)
    per_user = BooleanProperty(default=False)
    usage = BooleanProperty(default=False)


class BlockStorageQuota(Quota):
    """Resource limitations for Projects on Block Storage Services.

    Block Storage quota limitations apply on a Block Storage Service.

    Attributes:
    ----------
        id (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
    """

    type = StringProperty(default=ServiceType.BLOCK_STORAGE.value)
    gigabytes = IntegerProperty()
    per_volume_gigabytes = IntegerProperty()
    volumes = IntegerProperty()

    project = RelationshipFrom(
        "fedreg.project.models.Project", "HAS_USAGE_LIMITS", cardinality=One
    )
    service = RelationshipTo(
        "fedreg.service.models.BlockStorageService", "APPLIES_TO", cardinality=One
    )


class ComputeQuota(Quota):
    """Resource limitations for Projects on Compute Services.

    Compute quota limitations apply on a Compute Service.

    Attributes:
    ----------
        id (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        cores (int | None): Number of max usable cores.
        instance (int | None): Number of max VM instances.
        ram (int | None): Number of max usable RAM (MiB).
    """

    type = StringProperty(default=ServiceType.COMPUTE.value)
    cores = IntegerProperty()
    instances = IntegerProperty()
    ram = IntegerProperty()

    project = RelationshipFrom(
        "fedreg.project.models.Project", "HAS_USAGE_LIMITS", cardinality=One
    )
    service = RelationshipTo(
        "fedreg.service.models.ComputeService", "APPLIES_TO", cardinality=One
    )


class NetworkingQuota(Quota):
    """Resource limitations for Projects on Network Services.

    Network quota limitations apply on a Network Service.

    Attributes:
    ----------
        id (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        public_ips (int | None): The number of floating IP addresses allowed for each
            project.
        networks (int | None): The number of networks allowed for each project.
        ports (int | None): The number of ports allowed for each project.
        security_groups (int | None): The number of security groups allowed for each
            project.
        security_group_rules (int | None): The number of security group rules allowed
            for each project.
    """

    type = StringProperty(default=ServiceType.NETWORK.value)
    public_ips = IntegerProperty()
    networks = IntegerProperty()
    ports = IntegerProperty()
    security_groups = IntegerProperty()
    security_group_rules = IntegerProperty()

    project = RelationshipFrom(
        "fedreg.project.models.Project", "HAS_USAGE_LIMITS", cardinality=One
    )
    service = RelationshipTo(
        "fedreg.service.models.NetworkService", "APPLIES_TO", cardinality=One
    )


class ObjectStoreQuota(Quota):
    """Resource limitations for Projects on Object Storage Services.

    Object Storage quota limitations apply on a Object Storage Service.

    Attributes:
    ----------
        id (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
    """

    type = StringProperty(default=ServiceType.OBJECT_STORE.value)
    bytes = IntegerProperty()
    containers = IntegerProperty()
    objects = IntegerProperty()

    project = RelationshipFrom(
        "fedreg.project.models.Project", "HAS_USAGE_LIMITS", cardinality=One
    )
    service = RelationshipTo(
        "fedreg.service.models.ObjectStoreService", "APPLIES_TO", cardinality=One
    )
