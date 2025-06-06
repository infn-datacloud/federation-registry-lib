"""Neomodel model of the Region owned by a Provider."""

from neomodel import (
    FloatProperty,
    One,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
    ZeroOrMore,
)


class Region(StructuredNode):
    """Region owned by a Provider.

    A Region is used to split a provider resources and limit projects access.
    A Region can have a specific geographical location and supplies
    different services (compute, block storage, network..).

    Attributes:
    ----------
        id (uuid): AssociatedRegion unique ID.
        description (str): Brief description.
        name (str): Name of the Region in the Provider.
        overbooking_cpu (float): CPU overbooking factor.
        overbooking_ram (float): RAM overbooking factor.
        bandwidth_in (float): Bandwidth in.
        bandwidth_out (float): Bandwidth out.
    """

    id = UniqueIdProperty()
    description = StringProperty(default="")
    name = StringProperty(required=True)
    overbooking_cpu = FloatProperty(default=1.0)
    overbooking_ram = FloatProperty(default=1.0)
    bandwidth_in = FloatProperty(default=10.0)
    bandwidth_out = FloatProperty(default=10.0)

    provider = RelationshipFrom(
        "fedreg.provider.models.Provider", "DIVIDED_INTO", cardinality=One
    )
    services = RelationshipTo(
        "fedreg.service.models.Service", "SUPPLIES", cardinality=ZeroOrMore
    )

    def pre_delete(self):
        """Remove related services."""
        for item in self.services:
            item.delete()
