"""Neomodel models of the resource limitations for Projects on Services."""

from neomodel import (
    BooleanProperty,
    IntegerProperty,
    JSONProperty,
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
    type = StringProperty()

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
        pvcs (int | None): Number of max PVCs a user group can create
        storage (int | None): Max value for the sum of the "minimum required" gigabytes
            (GiB) for external storage.
        requests_ephemeral_storage (int | None): Max value for the sum of the "minimum
            required" gigabytes (GiB) for ephemeral storage.
        limits_ephemeral_storage (int | None): Max value for the sum of the "maximum
            usable" gigabytes (GiB) for ephemeral storage.
    """

    type = StringProperty(default=QuotaType.BLOCK_STORAGE.value)

    # Openstack specifics
    gigabytes = IntegerProperty()
    per_volume_gigabytes = IntegerProperty()
    volumes = IntegerProperty()

    # Kubernetes specifics
    pvcs = IntegerProperty()
    storage = IntegerProperty()
    requests_ephemeral_storage = IntegerProperty()
    limits_ephemeral_storage = IntegerProperty()

    service = RelationshipTo(
        "fedreg.service.models.BlockStorageService", "APPLY_TO", cardinality=One
    )


class StorageClassQuota(Quota):
    """Resource limitations for Projects on Block Storage Services.

    Block Storage quota limitations apply on a Block Storage Service.

    Attributes:
    ----------
        uid (int): Quota unique ID.
        description (str): Brief description.
        type (str): Quota type.
        per_user (str): This limitation should be applied to each user.
        usage (str): This quota defines the current resource usage.
        pvcs (int | None): Number of max PVCs a user group can create for a specific
            storageclass
        storage (int | None): Max value for the sum of the "minimum required" gigabytes
            (GiB) for a specific storageclass.
    """

    pvcs = IntegerProperty()
    storage = IntegerProperty()

    storageclass = RelationshipTo(
        "fedreg.v2.storageclass.models.StorageClass", "APPLIES_TO", cardinality=One
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
        limits_cpu (int | None): Max value for the sum of the maximum usable cpus
            for a pod.
        requests_cpu (int | None): Max value for the sum of the "minimum required" cpus
            for a pod.
        limits_memory (int | None): Max value for the sum of the maximum usable memory
            for a pod.
        requests_memory (int | None): Max value for the sum of the "minimum required"
            memory for a pod.
        pods (int | None): Max number of pods that can be created.
        gpus (dict[str, int] | None): For each type of GPU, define the maximum quota.
    """

    type = StringProperty(default=QuotaType.COMPUTE.value)

    # Openstack specifics
    cores = IntegerProperty()
    instances = IntegerProperty()
    ram = IntegerProperty()

    # Kubernetes specifics
    limits_cpu = IntegerProperty()
    requests_cpu = IntegerProperty()
    limits_memory = IntegerProperty()
    requests_memory = IntegerProperty()
    pods = IntegerProperty()
    gpus = JSONProperty()

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
