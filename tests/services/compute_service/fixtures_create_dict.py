"""ComputeService specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from app.provider.schemas_extended import (
    ComputeQuotaCreateExtended,
    FlavorCreateExtended,
    ImageCreateExtended,
)
from app.service.enum import ServiceType
from tests.flavor.utils import (
    IS_PUBLIC,
    random_flavor_required_attr,
    random_flavor_required_rel,
)
from tests.image.utils import random_image_required_attr, random_image_required_rel
from tests.quotas.compute_quota.utils import (
    random_compute_quota_required_attr,
    random_compute_quota_required_rel,
)
from tests.services.compute_service.utils import (
    random_compute_service_all_attr,
    random_compute_service_required_attr,
)

invalid_create_key_values = [
    ("description", None),
    ("type", None),
    ("type", ServiceType.BLOCK_STORAGE),
    ("type", ServiceType.IDENTITY),
    ("type", ServiceType.NETWORK),
    ("endpoint", None),
    ("name", None),
]


@fixture
def compute_service_create_minimum_data() -> Dict[str, Any]:
    """Dict with ComputeService mandatory attributes."""
    return random_compute_service_required_attr()


@fixture
@parametrize(attr=["flavors", "images", "quotas"])
def compute_service_create_data_passing_empty_list(attr: str) -> Dict[str, Any]:
    """Dict with all Region attributes.

    Passing an empty list is not a problem.
    """
    return {**random_compute_service_all_attr(), attr: []}


@fixture
@parametrize(is_public=IS_PUBLIC)
def compute_service_create_data_with_flavors(is_public: bool) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {
        **random_compute_service_all_attr(),
        "flavors": [
            FlavorCreateExtended(
                **random_flavor_required_attr(),
                **random_flavor_required_rel(is_public),
                is_public=is_public,
            )
        ],
    }


@fixture
@parametrize(is_public=IS_PUBLIC)
def compute_service_create_data_with_images(is_public: bool) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {
        **random_compute_service_all_attr(),
        "images": [
            ImageCreateExtended(
                **random_image_required_attr(),
                **random_image_required_rel(is_public),
                is_public=is_public,
            )
        ],
    }


@fixture
def compute_service_create_data_with_quotas() -> Dict[str, Any]:
    """Dict with relationships attributes."""
    quota = ComputeQuotaCreateExtended(
        **random_compute_quota_required_attr(), **random_compute_quota_required_rel()
    )
    return {**random_compute_service_all_attr(), "quotas": [quota]}


@fixture
def compute_service_create_data_with_2_quotas_same_proj() -> Dict[str, Any]:
    """Dict with 2 quotas on same project.

    A quota has the flag 'per_user' equals to True and the other equal to False.
    """
    quota1 = ComputeQuotaCreateExtended(
        **random_compute_quota_required_attr(), **random_compute_quota_required_rel()
    )
    quota2 = ComputeQuotaCreateExtended(
        **random_compute_quota_required_attr(),
        **random_compute_quota_required_rel(),
        per_user=not quota1.per_user,
    )
    return {**random_compute_service_all_attr(), "quotas": [quota1, quota2]}


@fixture
@parametrize("k, v", invalid_create_key_values)
def compute_service_create_invalid_pair(k: str, v: Any) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**random_compute_service_required_attr(), k: v}


@fixture
def compute_service_invalid_num_quotas_same_project() -> Dict[str, Any]:
    """Invalid number of quotas on same project.

    A project can have at most one `project` quota and one `per-user` quota on a
    specific service.
    """
    quota = ComputeQuotaCreateExtended(
        **random_compute_quota_required_attr(), **random_compute_quota_required_rel()
    )
    return {**random_compute_service_required_attr(), "quotas": [quota, quota]}


@fixture
def compute_service_create_duplicate_flavors() -> Dict[str, Any]:
    """Invalid case: the flavor list has duplicate values."""
    flavor = FlavorCreateExtended(**random_flavor_required_attr())
    return {**random_compute_service_required_attr(), "flavors": [flavor, flavor]}


@fixture
def compute_service_create_duplicate_images() -> Dict[str, Any]:
    """Invalid case: the image list has duplicate values."""
    image = ImageCreateExtended(**random_image_required_attr())
    return {**random_compute_service_required_attr(), "images": [image, image]}


compute_service_create_valid_data = fixture_union(
    "compute_service_create_valid_data",
    (
        compute_service_create_minimum_data,
        compute_service_create_data_with_flavors,
        compute_service_create_data_with_images,
        compute_service_create_data_with_quotas,
        compute_service_create_data_with_2_quotas_same_proj,
    ),
    idstyle="explicit",
)


compute_service_create_invalid_data = fixture_union(
    "compute_service_create_invalid_data",
    (
        compute_service_create_invalid_pair,
        compute_service_invalid_num_quotas_same_project,
        compute_service_create_duplicate_flavors,
        compute_service_create_duplicate_images,
    ),
    idstyle="explicit",
)
