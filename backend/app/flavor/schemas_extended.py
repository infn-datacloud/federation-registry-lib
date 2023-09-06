from app.flavor.schemas import FlavorRead, FlavorReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from pydantic import Field


class FlavorReadExtended(FlavorRead):
    """Model to extend the Flavor data read from the DB with the lists of
    related items for authenticated users."""

    provider: ProviderRead = Field(description="Provider owning this Flavor.")


class FlavorReadExtendedPublic(FlavorReadPublic):
    """Model to extend the Flavor data read from the DB with the lists of
    related items for non-authenticated users."""

    provider: ProviderReadPublic = Field(description="Provider owning this Flavor.")
