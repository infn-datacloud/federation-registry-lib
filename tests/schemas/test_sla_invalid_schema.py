from typing import Any

import pytest
from pytest_cases import parametrize_with_cases

from fed_reg.provider.schemas_extended import SLACreateExtended
from fed_reg.sla.models import SLA
from fed_reg.sla.schemas import SLABase, SLABasePublic, SLARead, SLAReadPublic
from tests.create_dict import sla_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_base_public(key: str, value: None) -> None:
    d = sla_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        SLABasePublic(**d)


@parametrize_with_cases("key, value")
def test_invalid_base(key: str, value: Any) -> None:
    d = sla_schema_dict()
    if key == "reversed_dates":
        tmp = d["end_date"]
        d["end_date"] = d["start_date"]
        d["start_date"] = tmp
    else:
        d[key] = value
    with pytest.raises(ValueError):
        SLABase(**d)


@parametrize_with_cases("key, value", has_tag="base_public")
def test_invalid_read_public(sla_model: SLA, key: str, value: str) -> None:
    sla_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        SLAReadPublic.from_orm(sla_model)


@parametrize_with_cases("key, value")
def test_invalid_read(sla_model: SLA, key: str, value: str) -> None:
    if key == "reversed_dates":
        tmp = sla_model.end_date
        sla_model.__setattr__("end_date", sla_model.start_date)
        sla_model.__setattr__("start_date", tmp)
    else:
        sla_model.__setattr__(key, value)
    with pytest.raises(ValueError):
        SLARead.from_orm(sla_model)


def test_invalid_create_extended() -> None:
    d = sla_schema_dict()
    with pytest.raises(ValueError):
        SLACreateExtended(**d)
