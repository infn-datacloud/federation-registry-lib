from neomodel import (
    StructuredNode,
    StringProperty,
    DateTimeProperty,
    UniqueIdProperty,
    RelationshipFrom,
    RelationshipTo,
    One,
)


class SLA(StructuredNode):
    """Flavor Base class.

    Class without id which is populated by the database.

    Attributes:
        id (int): Flavor unique ID.
        name (str): Flavor name.
        num_vcpus (int): Number of Virtual CPUs.
        num_gpus (int): Number of GPUs.
        ram (int): Reserved RAM (GB)
        disk (int): Reserved disk size (GB)
        infiniband_support (bool): #TODO: What is it?
    """

    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    description = StringProperty(default="")
    issue_date = DateTimeProperty(required=True)
    start_date = DateTimeProperty(required=True)
    end_date = DateTimeProperty(required=True)

    project = RelationshipFrom(
        ".Project", "REQUIRES_RESOURCES", cardinality=One
    )
    provider = RelationshipTo(
        ".Provider", "CAN_ACCESS_TO", cardinality=One
    )
