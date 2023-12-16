"""SLA specific fixtures."""
from typing import Any, Dict
from uuid import uuid4

from pytest_cases import fixture, fixture_union, parametrize

from tests.common.utils import random_lower_string, random_start_end_dates

invalid_create_key_values = [
    ("description", None),
    ("doc_uuid", None),
    ("start_date", None),
    ("end_date", None),
]


@fixture
def sla_create_mandatory_data() -> Dict[str, Any]:
    """Dict with SLA mandatory attributes."""
    start_date, end_date = random_start_end_dates()
    return {"doc_uuid": uuid4(), "start_date": start_date, "end_date": end_date}


@fixture
def sla_create_all_data(sla_create_mandatory_data: Dict[str, Any]) -> Dict[str, Any]:
    """Dict with all SLA attributes."""
    return {**sla_create_mandatory_data, "description": random_lower_string()}


@fixture
def sla_create_data_with_rel(sla_create_all_data: Dict[str, Any]) -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {**sla_create_all_data, "project": uuid4()}


@fixture
@parametrize("k, v", invalid_create_key_values)
def sla_create_invalid_pair(
    sla_create_mandatory_data: Dict[str, Any], k: str, v: Any
) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**sla_create_mandatory_data, k: v}


sla_create_valid_data = fixture_union(
    "sla_create_valid_data", (sla_create_data_with_rel,), idstyle="explicit"
)


sla_create_invalid_data = fixture_union(
    "sla_create_invalid_data",
    (sla_create_mandatory_data, sla_create_invalid_pair),
    idstyle="explicit",
)
