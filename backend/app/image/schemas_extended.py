from app.image.schemas import ImageRead, ImageReadPublic
from app.provider.schemas import ProviderRead, ProviderReadPublic
from pydantic import Field


class ImageReadExtended(ImageRead):
    """Model to extend the Image data read from the DB with the lists of
    related items for authenticated users."""

    provider: ProviderRead = Field(description="Provider owning this Image.")


class ImageReadExtendedPublic(ImageReadPublic):
    """Model to extend the Image data read from the DB with the lists of
    related items for non-authenticated users."""

    provider: ProviderReadPublic = Field(description="Provider owning this Image.")
