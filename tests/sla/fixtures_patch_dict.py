"""SLA specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.common.utils import random_date, random_lower_string
from tests.sla.utils import random_start_end_dates

patch_key_values = [
    ("description", random_lower_string()),
    ("doc_uuid", uuid4()),
    ("start_date", random_date()),
    ("end_date", random_date()),
]
invalid_patch_key_values = [  # None is not accepted because there is a default
    ("description", None),
]


@fixture
@parametrize("k, v", patch_key_values)
def sla_patch_valid_data(k: str, v: Any) -> Dict[str, Any]:
    """Valid set of single key-value pair for a SLA patch schema."""
    return {k: v}


@fixture
@parametrize("k, v", invalid_patch_key_values)
def sla_patch_invalid_single_attr(k: str, v: Any) -> Dict[str, Any]:
    """Invalid set of attributes for a SLA patch schema."""
    return {k: v}


@fixture
def sla_patch_invalid_dates_couple() -> Dict[str, Any]:
    """Valid set of single key-value pair for a SLA patch schema."""
    start_date, end_date = random_start_end_dates()
    return {"start_date": end_date, "end_date": start_date}


sla_patch_invalid_data = fixture_union(
    "sla_patch_invalid_data",
    (sla_patch_invalid_single_attr, sla_patch_invalid_dates_couple),
    idstyle="explicit",
)
