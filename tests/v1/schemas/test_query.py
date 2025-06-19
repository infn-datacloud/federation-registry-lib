from datetime import date, datetime
from enum import Enum
from typing import Literal

from pytest_cases import case, parametrize_with_cases

from fedreg.core import (
    BaseNode,
    create_query_model,
    get_field_basic_type,
    get_list_derived_attributes,
)
from tests.v1.utils import random_lower_string


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


class TestModelList(BaseNode):
    __test__ = False
    test_field: list[str]


class TestModelListNested(BaseNode):
    __test__ = False
    parent_field: list[TestModelStr]


class TestModelNested(BaseNode):
    __test__ = False
    parent_field: TestModelStr


class TestModelLiteral(BaseNode):
    __test__ = False
    test_field: Literal["pippo"]


class CaseModel:
    @case(tags=("str"))
    def case_model_str(self) -> type[TestModelStr]:
        return TestModelStr

    @case(tags=("str"))
    def case_model_enum(self) -> type[TestModelEnum]:
        return TestModelEnum

    @case(tags=("number"))
    def case_model_int(self) -> type[TestModelInt]:
        return TestModelInt

    @case(tags=("number"))
    def case_model_float(self) -> type[TestModelFloat]:
        return TestModelFloat

    @case(tags=("date"))
    def case_model_date(self) -> type[TestModelDate]:
        return TestModelDate

    @case(tags=("date"))
    def case_model_datetime(self) -> type[TestModelDateTime]:
        return TestModelDateTime

    @case(tags=("list"))
    def case_model_list(self) -> type[TestModelList]:
        return TestModelList

    @case(tags=("list_complex"))
    def case_model_list_nested(self) -> type[TestModelListNested]:
        return TestModelListNested

    @case(tags=("nested"))
    def case_model_nested(self) -> type[TestModelNested]:
        return TestModelNested

    @case(tags=("literal"))
    def case_model_origin(self) -> type[TestModelLiteral]:
        return TestModelLiteral


def test_field_type_generation():
    assert get_field_basic_type(TestModelStr.__fields__["test_field"].type_) == (
        str | None,
        None,
    )
    assert get_field_basic_type(TestModelEnum.__fields__["test_field"].type_) == (
        str | None,
        None,
    )
    assert get_field_basic_type(TestModelInt.__fields__["test_field"].type_) == (
        int | None,
        None,
    )
    assert get_field_basic_type(TestModelFloat.__fields__["test_field"].type_) == (
        float | None,
        None,
    )
    assert get_field_basic_type(TestModelDate.__fields__["test_field"].type_) == (
        date | None,
        None,
    )
    assert get_field_basic_type(TestModelDateTime.__fields__["test_field"].type_) == (
        datetime | None,
        None,
    )
    assert get_field_basic_type(TestModelList.__fields__["test_field"].type_) == (
        str | None,
        None,
    )
    assert (
        get_field_basic_type(TestModelListNested.__fields__["parent_field"].type_)
        is None
    )


def test_field_type_generation_from_list():
    field_name = "test_field"
    field_type = TestModelList.__fields__[field_name].type_
    new_field = (str | None, None)
    attributes = get_list_derived_attributes(
        new_field=new_field, field_name=field_name, field_type=field_type, deep=0
    )
    assert attributes.get(f"{field_name}__contains") == new_field
    assert attributes.get(f"{field_name}__icontains") == new_field


def test_field_type_generation_from_complex_list():
    field_name = "parent_field"
    child_field_name = "test_field"
    field_type = TestModelListNested.__fields__[field_name].type_
    new_field = None
    attributes = get_list_derived_attributes(
        new_field=new_field, field_name=field_name, field_type=field_type, deep=0
    )
    assert attributes.get(f"{field_name}_{child_field_name}") == new_field
    assert attributes.get(f"{field_name}_{child_field_name}__contains") == new_field
    assert attributes.get(f"{field_name}_{child_field_name}__icontains") == new_field
    assert attributes.get(f"{field_name}_{child_field_name}__startswith") == new_field
    assert attributes.get(f"{field_name}_{child_field_name}__istartswith") == new_field
    assert attributes.get(f"{field_name}_{child_field_name}__endswith") == new_field
    assert attributes.get(f"{field_name}_{child_field_name}__iendswith") == new_field
    assert attributes.get(f"{field_name}_{child_field_name}__regex") == new_field
    assert attributes.get(f"{field_name}_{child_field_name}__iregex") == new_field


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


@parametrize_with_cases("model", cases=CaseModel, has_tag="list")
def test_list(model: type[TestModelList]) -> None:
    cls = create_query_model(random_lower_string(), model)
    item = cls()
    assert not hasattr(item, "test_field")
    assert item.test_field__contains is None
    assert item.test_field__icontains is None


@parametrize_with_cases("model", cases=CaseModel, has_tag="list_complex")
def test_list_nested(model: type[TestModelListNested]) -> None:
    cls = create_query_model(random_lower_string(), model)
    item = cls()
    assert item.parent_field_test_field is None
    assert item.parent_field_test_field__contains is None
    assert item.parent_field_test_field__icontains is None
    assert item.parent_field_test_field__contains is None
    assert item.parent_field_test_field__icontains is None
    assert item.parent_field_test_field__startswith is None
    assert item.parent_field_test_field__istartswith is None
    assert item.parent_field_test_field__endswith is None
    assert item.parent_field_test_field__iendswith is None
    assert item.parent_field_test_field__regex is None
    assert item.parent_field_test_field__iregex is None


@parametrize_with_cases("model", cases=CaseModel, has_tag="nested")
def test_nested_model(model: type[TestModelNested]) -> None:
    cls = create_query_model(random_lower_string(), model)
    item = cls()
    assert item.parent_field_test_field is None
    assert item.parent_field_test_field__contains is None
    assert item.parent_field_test_field__icontains is None
    assert item.parent_field_test_field__startswith is None
    assert item.parent_field_test_field__istartswith is None
    assert item.parent_field_test_field__endswith is None
    assert item.parent_field_test_field__iendswith is None
    assert item.parent_field_test_field__regex is None
    assert item.parent_field_test_field__iregex is None


@parametrize_with_cases("model", cases=CaseModel, has_tag="literal")
def test_list_origin(model: type[TestModelLiteral]) -> None:
    cls = create_query_model(random_lower_string(), model)
    item = cls()
    assert not hasattr(item, "test_field")
