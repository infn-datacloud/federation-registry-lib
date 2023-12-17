"""SLA utilities."""
from datetime import date
from typing import Any, Dict, Tuple
from uuid import uuid4

from tests.common.utils import random_date, random_lower_string


def random_sla_required_attr() -> Dict[str, Any]:
    """Return a dict with the SLA required attributes initialized."""
    start_date, end_date = random_start_end_dates()
    return {"doc_uuid": uuid4(), "start_date": start_date, "end_date": end_date}


def random_sla_all_attr() -> Dict[str, Any]:
    """Dict with all SLA attributes."""
    return {**random_sla_required_attr(), "description": random_lower_string()}


def random_sla_required_rel() -> Dict[str, Any]:
    """Dict with SLA required relationships initialized."""
    return {"project": uuid4()}


def random_start_end_dates() -> Tuple[date, date]:
    """Return a random couples of valid start and end dates (in order)."""
    d1 = random_date()
    d2 = random_date()
    if d1 < d2:
        start_date = d1
        end_date = d2
    else:
        start_date = d2
        end_date = d1
    return start_date, end_date
