from neomodel import (
    StructuredNode,
    UniqueIdProperty,
    StringProperty,
    BooleanProperty,
    RelationshipFrom,
    One,
)


class Image(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty(default="")
    os = StringProperty(required=True) # TODO: add choices
    distribution = StringProperty(required=True)
    version = StringProperty(required=True)
    architecture = StringProperty(required=True)
    market_place = StringProperty(default="")
    cuda_support: BooleanProperty(default=False)
    gpu_driver: BooleanProperty(default=False)

    project = RelationshipFrom(
        ".Project", "AVAILABLE_VM_SIZE", cardinality=One
    )
