"""SLA specific fixtures."""
from typing import Any, Dict

from pytest_cases import fixture, fixture_union, parametrize

from tests.sla.utils import (
    random_sla_all_attr,
    random_sla_required_attr,
    random_sla_required_rel,
)

invalid_create_key_values = [
    ("description", None),
    ("doc_uuid", None),
    ("start_date", None),
    ("end_date", None),
]


@fixture
def sla_create_minimum_data() -> Dict[str, Any]:
    """Dict with SLA mandatory attributes."""
    return random_sla_required_attr()


@fixture
def sla_create_data_with_rel() -> Dict[str, Any]:
    """Dict with relationships attributes."""
    return {**random_sla_all_attr(), **random_sla_required_rel()}


@fixture
@parametrize("k, v", invalid_create_key_values)
def sla_create_invalid_pair(k: str, v: Any) -> Dict[str, Any]:
    """Dict with one invalid key-value pair."""
    return {**random_sla_required_attr(), **random_sla_required_rel(), k: v}


sla_create_valid_data = fixture_union(
    "sla_create_valid_data", (sla_create_data_with_rel,), idstyle="explicit"
)


sla_create_invalid_data = fixture_union(
    "sla_create_invalid_data",
    (sla_create_minimum_data, sla_create_invalid_pair),
    idstyle="explicit",
)
