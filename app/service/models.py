from neomodel import (
    OneOrMore,
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
    It is accessible through an endpoint. Authentication
    through IAM can be accepted. It can accept multiple
    authentication methods. It can be public or private.

    Attributes:
        uid (int): Service unique ID.
        name (str): Service name (type).
        description (str): Brief description.
        resource_type (str): Resource type.
        endpoint (str): URL pointing to this service
        iam_enabled (bool): IAM enabled for this service.
        is_public (bool): Public Service or not.
        public_ip_assignable (bool): It is possible to
            assign a public IP to this service.
        volume_types (list of str): TODO
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    endpoint = StringProperty(unique_index=True, required=True)

    provider = RelationshipFrom(
        "..provider.models.Provider", "PROVIDES_SERVICE", cardinality=OneOrMore
    )


class NovaService(Service):
    compute_time_quotas = RelationshipFrom(
        "..quota.models.ComputeTimeQuota", "APPLIES_TO", cardinality=ZeroOrMore
    )


class MesosService(Service):
    pass


class ChronosService(Service):
    pass


class MarathonService(Service):
    pass


class KubernetesService(Service):
    pass


class RucioService(Service):
    pass


class OneDataService(Service):
    pass
