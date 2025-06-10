"""Pydantic models of the Region owned by a Provider."""

from typing import Annotated

from pydantic import AnyHttpUrl, BaseModel, Field

from fedreg.v2.core import BaseNode, BaseNodeRead, PaginationQuery


class RegionBase(BaseNode):
    """Base schema for a region node in the provider.

    Attributes:
        name (str): Region name in the Provider.
        overbooking_cpu (float): CPU overbooking factor. Default is 1.0.
        overbooking_ram (float): RAM overbooking factor. Default is 1.0.
        bandwidth_in (float): Bandwidth in. Default is 10.0.
        bandwidth_out (float): Bandwidth out. Default is 10.0.
    """

    name: Annotated[str, Field(description="Region name in the Provider.")]
    overbooking_cpu: Annotated[
        float, Field(default=1.0, description="CPU overbooking factor.")
    ]
    overbooking_ram: Annotated[
        float, Field(default=1.0, description="RAM overbooking factor.")
    ]
    bandwidth_in: Annotated[float, Field(default=10.0, description="Bandwidth in.")]
    bandwidth_out: Annotated[float, Field(default=10.0, description="Bandwidth out.")]


class RegionCreate(RegionBase):
    """Schema for creating a new Region.

    Inherits from:
        RegionBase: Base schema containing common region attributes.

    Attributes:
        Inherits all fields from RegionBase.
    """


class RegionLinks(BaseModel):
    """
    Represents hyperlinks related to a Region.

    Attributes:
        services (AnyHttpUrl): Link to the services provided by the Region.
    """

    services: Annotated[
        AnyHttpUrl, Field(description="Link to the services provided by the Region.")
    ]


class RegionRead(BaseNodeRead, RegionBase):
    """Represents a read-only view of a Region, extending BaseNodeRead and RegionBase.

    Attributes:
        services (list[str]): List of services provided by the Region.
        links (RegionLinks): Links to the Region resources.
    """

    services: Annotated[
        list[str],
        Field(
            default_factory=list,
            description="List of services provided by the Region.",
        ),
    ]
    links: Annotated[
        RegionLinks,
        Field(
            description="Links to the Region resources.",
        ),
    ]


class RegionQuery(PaginationQuery):
    """Model for filtering regions based on various attributes.

    Attributes:
        name (str | None): Region name in the Provider.
        overbooking_cpu (float | None): CPU overbooking factor.
        overbooking_ram (float | None): RAM overbooking factor.
        bandwidth_in (float | None): Bandwidth in.
        bandwidth_out (float | None): Bandwidth out.
    """

    name: Annotated[
        str | None, Field(default=None, description="Region name in the Provider.")
    ]
    overbooking_cpu: Annotated[
        float | None, Field(default=None, description="CPU overbooking factor.")
    ]
    overbooking_ram: Annotated[
        float | None, Field(default=None, description="RAM overbooking factor.")
    ]
    bandwidth_in: Annotated[
        float | None, Field(default=None, description="Bandwidth in.")
    ]
    bandwidth_out: Annotated[
        float | None, Field(default=None, description="Bandwidth out.")
    ]
