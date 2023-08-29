from neomodel import (
    FloatProperty,
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)


class Location(StructuredNode):
    """Location class.

    Providers can have a Geographical location.

    Attributes:
        uid (int): Location unique ID.
        description (str): Brief description.
        name (str): Location unique name.
        country (str): Country name.
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    name = StringProperty(unique_index=True, required=True)
    country = StringProperty(required=True)
    latitude = FloatProperty()
    longitude = FloatProperty()

    providers = RelationshipFrom(
        "..provider.models.Provider", "LOCATED_AT", cardinality=ZeroOrMore
    )
