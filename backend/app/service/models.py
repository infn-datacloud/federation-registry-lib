from neomodel import (
    One,
    RelationshipFrom,
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

    provider = RelationshipFrom(
        "..provider.models.Provider", "SUPPLY", cardinality=One
    )


class NovaService(Service):
    num_cpu_quotas = RelationshipFrom(
        "..quota.models.NumCPUQuota", "APPLY_TO", cardinality=ZeroOrMore
    )
    # instances_quotas = RelationshipFrom(
    #    "..quota.models.InstanceQuota", "APPLY_TO", cardinality=ZeroOrMore
    # )
    # key_pairs_quotas = RelationshipFrom(
    #    "..quota.models.KeyPairQuota", "APPLY_TO", cardinality=ZeroOrMore
    # )
    # metadata_quotas = RelationshipFrom(
    #    "..quota.models.MetadataItemsQuota",
    #    "APPLY_TO",
    #    cardinality=ZeroOrMore,
    # )
    ram_quotas = RelationshipFrom(
        "..quota.models.RAMQuota", "APPLY_TO", cardinality=ZeroOrMore
    )
    # server_group_quotas = RelationshipFrom(
    #    "..quota.models.ServerGroupQuota", "APPLY_TO", cardinality=ZeroOrMore
    # )
    # server_group_members_quotas = RelationshipFrom(
    #    "..quota.models.ServerGroupMemberQuota",
    #    "APPLY_TO",
    #    cardinality=ZeroOrMore,
    # )


class MesosService(Service):
    pass


class ChronosService(Service):
    pass


class MarathonService(Service):
    pass


class KubernetesService(Service):
    num_cpu_quotas = RelationshipFrom(
        "..quota.models.NumCPUQuota", "APPLY_TO", cardinality=ZeroOrMore
    )
    ram_quotas = RelationshipFrom(
        "..quota.models.RAMQuota", "APPLY_TO", cardinality=ZeroOrMore
    )


class RucioService(Service):
    pass


class OneDataService(Service):
    pass
