import pytest

from app.flavor.crud import flavor
from app.flavor.schemas import FlavorBase, FlavorUpdate
from app.provider.schemas_extended import FlavorCreateExtended
from tests.flavor.controller import FlavorController


@pytest.fixture(scope="module")
def flavor_controller() -> FlavorController:
    return FlavorController(
        base_schema=FlavorBase,
        base_public_schema=FlavorBase,
        create_schema=FlavorCreateExtended,
        update_schema=FlavorUpdate,
        crud=flavor,
        endpoint_group="flavors",
        item_name="Flavor",
    )
