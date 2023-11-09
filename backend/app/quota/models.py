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
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    type = StringProperty(required=True)
    per_user = BooleanProperty(default=False)

    project = RelationshipFrom(
        "..project.models.Project", "USE_SERVICE_WITH", cardinality=One
    )


class BlockStorageQuota(Quota):
    """Resource limitations for Projects on Block Storage Services.

    Block Storage quota limitations apply on a Block Storage Service.

    Attributes:
    ----------
        gigabytes (int): Number of max usable gigabytes (GiB).
        per_volume_gigabytes (int): Number of max usable gigabytes per volume (GiB).
        volumes (int): Number of max volumes a user group can create.
    """

    gigabytes = IntegerProperty()
    per_volume_gigabytes = IntegerProperty()
    volumes = IntegerProperty()

    service = RelationshipTo(
        "..service.models.BlockStorageService", "APPLY_TO", cardinality=One
    )


class ComputeQuota(Quota):
    """Resource limitations for Projects on Compute Services.

    Compute quota limitations apply on a Compute Service.

    Attributes:
    ----------
        cores (int): Number of max usable cores.
        instance (int): Number of max VM instances.
        ram (int): Number of max usable RAM (MiB).
    """

    cores = IntegerProperty()
    instances = IntegerProperty()
    ram = IntegerProperty()

    service = RelationshipTo(
        "..service.models.ComputeService", "APPLY_TO", cardinality=One
    )


class NetworkQuota(Quota):
    """Resource limitations for Projects on Network Services.

    Network quota limitations apply on a Network Service.

    Attributes:
    ----------
        public_ips (int): The number of floating IP addresses allowed for each project.
        networks (int): The number of networks allowed for each project.
        port (int): The number of ports allowed for each project.
        security_groups (int): The number of security groups allowed for each project.
        security_group_rules (int): The number of security group rules allowed for each
            project.
    """

    public_ips = IntegerProperty()
    networks = IntegerProperty()
    ports = IntegerProperty()
    security_groups = IntegerProperty()
    security_group_rules = IntegerProperty()

    service = RelationshipTo(
        "..service.models.NetworkService", "APPLY_TO", cardinality=One
    )
