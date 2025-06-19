"""Neomodel model of the site geographical Location."""

from neomodel import (
    FloatProperty,
    RelationshipFrom,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)


class Location(StructuredNode):
    """Site geographical Location.

    Providers or single Regions can have a Geographical location.

    Attributes:
    ----------
        uid (int): Location unique ID.
        description (str): Brief description.
        site (str): Location unique name.
        country (str): Country name.
        latitude (float | None): Latitude coordinate.
        longitude (float | None): Longitude coordinate.
    """

    uid = UniqueIdProperty()
    description = StringProperty(default="")
    site = StringProperty(unique_index=True, required=True)
    country = StringProperty(required=True)
    latitude = FloatProperty()
    longitude = FloatProperty()

    regions = RelationshipFrom(
        "fedreg.region.models.Region", "LOCATED_AT", cardinality=ZeroOrMore
    )
