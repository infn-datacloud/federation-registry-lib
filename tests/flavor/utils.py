"""Flavor specific fixtures."""
from app.flavor.models import Flavor
from app.flavor.schemas import (
    FlavorBase,
    FlavorBasePublic,
    FlavorRead,
    FlavorReadPublic,
)
from app.flavor.schemas_extended import FlavorReadExtended, FlavorReadExtendedPublic
from app.provider.schemas_extended import FlavorCreateExtended
from tests.flavor.schema_validators import (
    BaseSchemaValidation,
    CreateSchemaValidation,
    ReadSchemaValidation,
)


class BaseFlavorValidation(BaseSchemaValidation[FlavorBase, FlavorBasePublic]):
    """Base class to validate Flavor schemas."""


class CreateFlavorValidation(
    CreateSchemaValidation[FlavorBase, FlavorBasePublic, FlavorCreateExtended]
):
    """Class to validate Flavor Create schemas."""


class ReadFlavorValidation(
    ReadSchemaValidation[
        FlavorBase,
        FlavorBasePublic,
        FlavorRead,
        FlavorReadPublic,
        FlavorReadExtended,
        FlavorReadExtendedPublic,
        Flavor,
    ]
):
    """Class to validate Flavor Read schemas."""
