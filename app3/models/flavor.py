from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    BooleanProperty,
    UniqueIdProperty,
    RelationshipFrom,
    One,
)


class Flavor(StructuredNode):
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
    num_vcpus = IntegerProperty(default=0)
    num_gpus = IntegerProperty(default=0)
    ram = IntegerProperty(default=0)
    disk = IntegerProperty(default=0)
    infiniband_support = BooleanProperty(default=False)  # TODO: What is it?

    project = RelationshipFrom(
        ".Project", "AVAILABLE_VM_SIZE", cardinality=One
    )
