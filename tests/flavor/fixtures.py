from typing import Any, Dict

import pytest
from pytest_cases import fixture, parametrize_with_cases

from app.flavor.crud import flavor_mng
from app.flavor.models import Flavor
from app.flavor.schemas import FlavorBase, FlavorUpdate
from app.provider.schemas_extended import FlavorCreateExtended
from app.service.models import ComputeService
from tests.flavor.controller import FlavorController
from tests.flavor.schema import ValidData


@pytest.fixture(scope="module")
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


@fixture
@parametrize_with_cases("data", cases=ValidData)
def db_item(data: Dict[str, Any], db_compute_serv: ComputeService) -> Flavor:
    """Fixture with standard Flavor."""
    item = FlavorCreateExtended(**data)
    return flavor_mng.create(obj_in=item, service=db_compute_serv)
