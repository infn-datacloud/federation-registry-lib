from datetime import date, datetime
from enum import Enum
from typing import Type

from pytest_cases import case, parametrize_with_cases

from fed_reg.models import BaseNode
from fed_reg.query import create_query_model
from tests.utils import random_lower_string


class TestModelBool(BaseNode):
    __test__ = False
    test_field: bool


class TestModelInt(BaseNode):
    __test__ = False
    test_field: int


class TestModelFloat(BaseNode):
    __test__ = False
    test_field: float


class TestModelDate(BaseNode):
    __test__ = False
    test_field: date


class TestModelDateTime(BaseNode):
    __test__ = False
    test_field: datetime


class TestModelStr(BaseNode):
    __test__ = False
    test_field: str


class TestEnum(Enum):
    __test__ = False
    VALUE_1 = "value_1"
    VALUE_2 = "value_2"


class TestModelEnum(BaseNode):
    __test__ = False
    test_field: TestEnum


class CaseModel:
    @case(tags=["str"])
    def case_model_str(self) -> Type[TestModelStr]:
        return TestModelStr

    @case(tags=["str"])
    def case_model_enum(self) -> Type[TestModelEnum]:
        return TestModelEnum

    @case(tags=["number"])
    def case_model_int(self) -> Type[TestModelInt]:
        return TestModelInt

    @case(tags=["number"])
    def case_model_float(self) -> Type[TestModelFloat]:
        return TestModelFloat

    @case(tags=["date"])
    def case_model_date(self) -> Type[TestModelDate]:
        return TestModelDate

    @case(tags=["date"])
    def case_model_datetime(self) -> Type[TestModelDateTime]:
        return TestModelDateTime


def test_bool() -> None:
    cls = create_query_model(random_lower_string(), TestModelBool)
    item = cls()
    assert item.test_field is None


@parametrize_with_cases("model", cases=CaseModel, has_tag="number")
def test_numbers(model: type[TestModelInt] | type[TestModelFloat]) -> None:
    cls = create_query_model(random_lower_string(), model)
    item = cls()
    assert item.test_field is None
    assert item.test_field__lt is None
    assert item.test_field__gt is None
    assert item.test_field__lte is None
    assert item.test_field__gte is None
    assert item.test_field__ne is None


@parametrize_with_cases("model", cases=CaseModel, has_tag="date")
def test_dates(model: type[TestModelDate] | type[TestModelDateTime]) -> None:
    cls = create_query_model(random_lower_string(), model)
    item = cls()
    assert item.test_field__lt is None
    assert item.test_field__gt is None
    assert item.test_field__lte is None
    assert item.test_field__gte is None
    assert item.test_field__ne is None


@parametrize_with_cases("model", cases=CaseModel, has_tag="str")
def test_str_enum(model: type[TestModelStr] | type[TestModelEnum]) -> None:
    cls = create_query_model(random_lower_string(), model)
    item = cls()
    assert item.test_field is None
    assert item.test_field__contains is None
    assert item.test_field__icontains is None
    assert item.test_field__startswith is None
    assert item.test_field__istartswith is None
    assert item.test_field__endswith is None
    assert item.test_field__iendswith is None
    assert item.test_field__regex is None
    assert item.test_field__iregex is None


# TODO test lists
# TODO test get_origin(v.type_)
# TODO test else case
