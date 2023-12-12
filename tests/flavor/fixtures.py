"""Flavor specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

import pytest
from pytest_cases import fixture, parametrize

from app.flavor.crud import flavor_mng
from app.flavor.models import Flavor
from app.flavor.schemas import FlavorBase, FlavorUpdate
from app.provider.models import Provider
from app.provider.schemas_extended import FlavorCreateExtended
from app.region.models import Region
from app.service.models import ComputeService
from tests.flavor.controller import FlavorController
from tests.utils.utils import (
    random_bool,
    random_lower_string,
    random_non_negative_int,
    random_positive_int,
)

is_public = {True, False}
zero_or_more_rels = {0, 1, 2}


@pytest.fixture(scope="package")
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


@fixture(scope="package")
def data_mandatory() -> Dict[str, Any]:
    """Dict with Flavor mandatory attributes."""
    return {"name": random_lower_string(), "uuid": uuid4()}


@fixture(scope="package")
@parametrize("is_public", is_public)
def data_all(is_public: bool, data_mandatory: Dict[str, Any]) -> Dict[str, Any]:
    """Dict with all Flavor attributes.

    Attribute is_public has been parametrized.
    """
    return {
        **data_mandatory,
        "is_public": is_public,
        "description": random_lower_string(),
        "disk": random_non_negative_int(),
        "ram": random_non_negative_int(),
        "vcpus": random_non_negative_int(),
        "swap": random_non_negative_int(),
        "ephemeral": random_non_negative_int(),
        "infiniband": random_bool(),
        "gpus": random_positive_int(),
        "gpu_model": random_lower_string(),
        "gpu_vendor": random_lower_string(),
        "local_storage": random_lower_string(),
    }


@fixture
@parametrize("owned_projects", zero_or_more_rels)
def db_flavor(
    owned_projects: int,
    data_mandatory: Dict[str, Any],
    db_compute_serv2: ComputeService,
) -> Flavor:
    """Fixture with standard DB Flavor.

    The flavor can be public or private based on the number of allowed projects.
    0 - Public. 1 or 2 - Private.
    """
    db_region: Region = db_compute_serv2.region.single()
    db_provider: Provider = db_region.provider.single()
    projects = [i.uuid for i in db_provider.projects]
    item = FlavorCreateExtended(
        **data_mandatory,
        is_public=owned_projects == 0,
        projects=projects[:owned_projects],
    )
    return flavor_mng.create(obj_in=item, service=db_compute_serv2)


@fixture
def db_shared_flavor(
    data_mandatory: Dict[str, Any], db_flavor: Flavor, db_compute_serv3: ComputeService
) -> Flavor:
    """Flavor shared within multiple services."""
    projects = [i.uuid for i in db_flavor.projects]
    item = FlavorCreateExtended(
        **data_mandatory, is_public=len(projects) == 0, projects=projects
    )
    return flavor_mng.create(obj_in=item, service=db_compute_serv3)
