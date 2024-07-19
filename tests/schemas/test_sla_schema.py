from typing import Any
from uuid import uuid4

from pytest_cases import parametrize_with_cases

from fed_reg.provider.schemas_extended import SLACreateExtended
from fed_reg.sla.models import SLA
from fed_reg.sla.schemas import (
    SLABase,
    SLABasePublic,
    SLARead,
    SLAReadPublic,
    SLAUpdate,
)
from tests.create_dict import sla_schema_dict


@parametrize_with_cases("key, value", has_tag="base_public")
def test_base_public(key: str, value: str) -> None:
    d = sla_schema_dict()
    if key:
        d[key] = value
    item = SLABasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.doc_uuid == d.get("doc_uuid").hex


@parametrize_with_cases("key, value", has_tag="base")
def test_base(key: str, value: Any) -> None:
    d = sla_schema_dict()
    if key:
        d[key] = value
        if key.startswith("gpu_"):
            d["gpus"] = 1
    item = SLABase(**d)
    assert item.doc_uuid == d.get("doc_uuid").hex
    assert item.start_date == d.get("start_date")
    assert item.end_date == d.get("end_date")


@parametrize_with_cases("key, value", has_tag="update")
def test_update(key: str, value: Any) -> None:
    d = sla_schema_dict()
    if key:
        d[key] = value
    item = SLAUpdate(**d)
    assert item.doc_uuid == (d.get("doc_uuid").hex if d.get("doc_uuid") else None)
    assert item.start_date == d.get("start_date")
    assert item.end_date == d.get("end_date")


@parametrize_with_cases("key, value", has_tag="base_public")
def test_read_public(sla_model: SLA, key: str, value: str) -> None:
    if key:
        sla_model.__setattr__(key, value)
    item = SLAReadPublic.from_orm(sla_model)

    assert item.uid
    assert item.uid == sla_model.uid
    assert item.description == sla_model.description
    assert item.doc_uuid == sla_model.doc_uuid


@parametrize_with_cases("key, value", has_tag="base")
def test_read(sla_model: SLA, key: str, value: Any) -> None:
    if key:
        sla_model.__setattr__(key, value)
    item = SLARead.from_orm(sla_model)

    assert item.uid
    assert item.uid == sla_model.uid
    assert item.description == sla_model.description
    assert item.doc_uuid == sla_model.doc_uuid
    assert item.start_date == sla_model.start_date
    assert item.end_date == sla_model.end_date


def test_create_extended() -> None:
    d = sla_schema_dict()
    d["project"] = uuid4()
    item = SLACreateExtended(**d)
    assert item.project == d["project"].hex


# TODO Test read extended classes
