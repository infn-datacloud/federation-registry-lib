from neomodel import (
    FloatProperty,
    OneOrMore,
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)


class Location(StructuredNode):
    """Location class.

    Providers can have a Geographical location.

    Attributes:
        uid (int): Location unique ID.
        description (str): Brief description.
        site (str): Location unique name.
        country (str): Country name.
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    site = StringProperty(unique_index=True, required=True)
    country = StringProperty(required=True)
    latitude = FloatProperty()
    longitude = FloatProperty()

    regions = RelationshipFrom(
        "..region.models.Region", "LOCATED_AT", cardinality=OneOrMore
    )
