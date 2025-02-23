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

from fedreg.quota.enum import QuotaType


class Quota(StructuredNode):
    """Resource limitations for Projects on Services.

    Common attributes to all quota types.
    Any quota belongs to a only a project.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    per_user = BooleanProperty(default=False)
    usage = BooleanProperty(default=False)

    project = RelationshipFrom(
        "fedreg.project.models.Project", "USE_SERVICE_WITH", cardinality=One
    )


class BlockStorageQuota(Quota):
    """Resource limitations for Projects on Block Storage Services.

    Block Storage quota limitations apply on a Block Storage Service.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        gigabytes (int | None): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int | None): Number of max usable gigabytes per volume
            (GiB).
        volumes (int | None): Number of max volumes a user group can create.
    """

    type = StringProperty(default=QuotaType.BLOCK_STORAGE.value)
    gigabytes = IntegerProperty()
    per_volume_gigabytes = IntegerProperty()
    volumes = IntegerProperty()

    service = RelationshipTo(
        "fedreg.service.models.BlockStorageService", "APPLY_TO", cardinality=One
    )


class ComputeQuota(Quota):
    """Resource limitations for Projects on Compute Services.

    Compute quota limitations apply on a Compute Service.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        cores (int | None): Number of max usable cores.
        instance (int | None): Number of max VM instances.
        ram (int | None): Number of max usable RAM (MiB).
    """

    type = StringProperty(default=QuotaType.COMPUTE.value)
    cores = IntegerProperty()
    instances = IntegerProperty()
    ram = IntegerProperty()

    service = RelationshipTo(
        "fedreg.service.models.ComputeService", "APPLY_TO", cardinality=One
    )


class NetworkQuota(Quota):
    """Resource limitations for Projects on Network Services.

    Network quota limitations apply on a Network Service.

    Attributes:
    ----------
        uid (int): Quota unique ID.
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

    type = StringProperty(default=QuotaType.NETWORK.value)
    public_ips = IntegerProperty()
    networks = IntegerProperty()
    ports = IntegerProperty()
    security_groups = IntegerProperty()
    security_group_rules = IntegerProperty()

    service = RelationshipTo(
        "fedreg.service.models.NetworkService", "APPLY_TO", cardinality=One
    )


class ObjectStoreQuota(Quota):
    """Resource limitations for Projects on Object Storage Services.

    Object Storage quota limitations apply on a Object Storage Service.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
    """

    type = StringProperty(default=QuotaType.OBJECT_STORE.value)
    bytes = IntegerProperty()
    containers = IntegerProperty()
    objects = IntegerProperty()

    service = RelationshipTo(
        "fedreg.service.models.ObjectStoreService", "APPLY_TO", cardinality=One
    )
