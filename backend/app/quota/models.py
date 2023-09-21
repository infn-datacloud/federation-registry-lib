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
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    type = StringProperty(required=True)
    per_user = BooleanProperty(default=False)

    project = RelationshipFrom(
        "..project.models.Project", "USE_SERVICE_WITH", cardinality=One
    )


class ComputeQuota(Quota):
    cores = IntegerProperty()
    fixed_ips = IntegerProperty()
    public_ips = IntegerProperty()
    instances = IntegerProperty()
    ram = IntegerProperty()

    service = RelationshipTo(
        "..service.models.ComputeService", "APPLY_TO", cardinality=One
    )


class BlockStorageQuota(Quota):
    gigabytes = IntegerProperty()
    per_volume_gigabytes = IntegerProperty()
    volumes = IntegerProperty()

    service = RelationshipTo(
        "..service.models.BlockStorageService", "APPLY_TO", cardinality=One
    )
