from typing import Any, Literal, Tuple
from uuid import uuid4

import pytest
from pytest_cases import case, parametrize, parametrize_with_cases

from fed_reg.models import BaseNode, BaseNodeCreate, BaseNodeQuery
from fed_reg.provider.schemas_extended import SLACreateExtended
from fed_reg.sla.schemas import (
    SLABase,
    SLABasePublic,
    SLACreate,
    SLAQuery,
    SLAUpdate,
)
from tests.create_dict import sla_schema_dict
from tests.utils import random_lower_string


class CaseAttr:
    @case(tags=["base_public", "update"])
    def case_none(self) -> Tuple[None, None]:
        return None, None

    @case(tags=["base_public"])
    def case_desc(self) -> Tuple[Literal["description"], str]:
        return "description", random_lower_string()


class CaseInvalidAttr:
    @case(tags=["base_public", "update"])
    def case_attr(self) -> Tuple[Literal["doc_uuid"], None]:
        return "doc_uuid", None

    @case(tags=["update"])
    @parametrize(attr=["start_date", "end_date"])
    def case_nullable_dates(self, attr: str) -> Tuple[str, None]:
        return attr, None

    def case_reversed_dates(self) -> Tuple[Literal["reversed_dates"], None]:
        return "reversed_dates", None


@parametrize_with_cases("key, value", cases=CaseAttr, has_tag=["base_public"])
def test_base_public(key: str, value: str) -> None:
    assert issubclass(SLABasePublic, BaseNode)
    d = sla_schema_dict()
    if key:
        d[key] = value
    item = SLABasePublic(**d)
    assert item.description == d.get("description", "")
    assert item.doc_uuid == d.get("doc_uuid").hex


@parametrize_with_cases("key, value", cases=CaseInvalidAttr, has_tag=["base_public"])
def test_invalid_base_public(key: str, value: None) -> None:
    d = sla_schema_dict()
    d[key] = value
    with pytest.raises(ValueError):
        SLABasePublic(**d)


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_base(key: str, value: Any) -> None:
    assert issubclass(SLABase, SLABasePublic)
    d = sla_schema_dict()
    if key:
        d[key] = value
        if key.startswith("gpu_"):
            d["gpus"] = 1
    item = SLABase(**d)
    assert item.doc_uuid == d.get("doc_uuid").hex
    assert item.start_date == d.get("start_date")
    assert item.end_date == d.get("end_date")


@parametrize_with_cases("key, value", cases=CaseInvalidAttr)
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


def test_create() -> None:
    assert issubclass(SLACreate, BaseNodeCreate)
    assert issubclass(SLACreate, SLABase)


@parametrize_with_cases(
    "key, value", cases=[CaseInvalidAttr, CaseAttr], has_tag=["update"]
)
def test_update(key: str, value: Any) -> None:
    assert issubclass(SLAUpdate, BaseNodeCreate)
    assert issubclass(SLAUpdate, SLABase)
    d = sla_schema_dict()
    if key:
        d[key] = value
    item = SLAUpdate(**d)
    assert item.doc_uuid == (d.get("doc_uuid").hex if d.get("doc_uuid") else None)
    assert item.start_date == d.get("start_date")
    assert item.end_date == d.get("end_date")


def test_query() -> None:
    assert issubclass(SLAQuery, BaseNodeQuery)


def test_create_extended() -> None:
    assert issubclass(SLACreateExtended, SLACreate)
    d = sla_schema_dict()
    d["project"] = uuid4()
    item = SLACreateExtended(**d)
    assert item.project == d["project"].hex


def test_invalid_create_extended() -> None:
    d = sla_schema_dict()
    with pytest.raises(ValueError):
        SLACreateExtended(**d)


# TODO Test all read classes
