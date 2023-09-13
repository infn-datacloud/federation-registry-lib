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
    """Associated Project class.

    Relationship linking a user group to a provider.
    This link correspond to a "project/tenant" entity.

    Attributes:
        name (str): Quota name (type).
        description (str): Brief description.
        tot_limit (float | None): The max quantity of a resource to
            be granted to the user group in total. TODO
        instance_limit (float | None): The max quantity of a resource
            to be granted to each VM/Container instance. TODO
        user_limit (float | None): The max quantity of a resource to
            be granted to user. TODO
        tot_guaranteed (float): The guaranteed quantity of a
            resource to be granted to the user group in total. TODO
        instance_guaranteed (float): The guaranteed quantity
            of a resource to be granted to each VM/Container
            instance. TODO
        user_guaranteed (float): The guaranteed quantity
            of a resource to be granted to user. TODO
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    type = StringProperty(required=True)

    project = RelationshipFrom(
        "..project.models.Project", "USE_SERVICE_WITH", cardinality=One
    )


class NovaQuota(Quota):
    cores = IntegerProperty()
    fixed_ips = IntegerProperty()
    floating_ips = IntegerProperty()
    force = BooleanProperty()
    injected_file_content_bytes = IntegerProperty()
    injected_file_path_bytes = IntegerProperty()
    injected_files = IntegerProperty()
    instances = IntegerProperty()
    key_pairs = IntegerProperty()
    metadata_items = IntegerProperty()
    networks = IntegerProperty()
    ram = IntegerProperty()
    security_group_rules = IntegerProperty()
    security_groups = IntegerProperty()
    server_groups = IntegerProperty()
    server_group_members = IntegerProperty()

    service = RelationshipTo(
        "..service.models.NovaService", "APPLY_TO", cardinality=One
    )


class CinderQuota(Quota):
    backup_gigabytes = IntegerProperty()
    backups = IntegerProperty()
    gigabytes = IntegerProperty()
    groups = IntegerProperty()
    per_volume_gigabytes = IntegerProperty()
    snapshots = IntegerProperty()
    volumes = IntegerProperty()

    service = RelationshipTo(
        "..service.models.CinderService", "APPLY_TO", cardinality=One
    )
