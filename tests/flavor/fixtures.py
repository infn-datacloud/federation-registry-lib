"""Flavor specific fixtures."""
import pytest

from app.flavor.crud import flavor_mng
from app.flavor.schemas import FlavorBase, FlavorUpdate
from app.provider.schemas_extended import FlavorCreateExtended
from tests.flavor.controller import FlavorController


@pytest.fixture
def flavor_controller() -> FlavorController:
    return FlavorController(
        base_schema=FlavorBase,
        base_public_schema=FlavorBase,
        create_schema=FlavorCreateExtended,
        update_schema=FlavorUpdate,
        crud=flavor_mng,
        endpoint_group="flavors",
        item_name="Flavor",
    )
