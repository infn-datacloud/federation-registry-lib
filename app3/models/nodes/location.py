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
        name (str): Location unique name.
        description (str): Brief description.
        country (str): Country name.
        country_code (str): Country code.
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.
    """

    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    description = StringProperty(default="")
    country = StringProperty(required=True)
    country_code = StringProperty(required=True)
    latitude = FloatProperty(required=True)
    longitude = FloatProperty(required=True)

    providers = RelationshipFrom(
        ".Provider", "LOCATED_AT", cardinality=OneOrMore
    )
