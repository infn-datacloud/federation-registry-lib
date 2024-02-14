from random import randint
from typing import Any, Literal, Optional, Tuple

import pytest
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.query import DbQueryCommonParams, Pagination, SchemaSize


class CaseSchemaSizeAttr:
    @parametrize(key=["short", "with_conn"])
    def case_key(self, key: str) -> str:
        return key


class CasePaginationAttr:
    @parametrize(key=["page", "size"])
    def case_key(self, key: str) -> str:
        return key


class CasePaginationInvalidAttr:
    @parametrize(value=[None, -1])
    def case_page(self, value: Optional[int]) -> Tuple[Literal["page"], Optional[int]]:
        return "page", value

    @parametrize(value=[-1, 0])
    def case_size(self, value: Optional[int]) -> Tuple[Literal["size"], Optional[int]]:
        return "size", value


class CaseDbQueryAttr:
    def case_skip(self) -> Tuple[Literal["skip"], int]:
        return "skip", randint(0, 100)

    def case_limit(self) -> Tuple[Literal["limit"], int]:
        return "limit", randint(0, 100)

    @parametrize(key=["limit", "sort"])
    def case_none(self, key: str) -> Tuple[str, None]:
        return key, None


class CaseSort:
    @parametrize(value=["test", "test_asc"])
    def case_sort_asc(self, value: str) -> Tuple[str]:
        return value, "test"

    @parametrize(value=["test_desc", "-test", "-test_desc"])
    def case_sort_desc(self, value: str) -> Tuple[str]:
        return value, "-test"


class CaseDbQueryInvalidAttr:
    @parametrize(value=[None, -1])
    def case_skip(self, value) -> Tuple[Literal["skip"], Optional[int]]:
        return "skip", value

    def case_limit(self) -> Tuple[Literal["limit"], int]:
        return "limit", -1


def test_default_schema() -> None:
    item = SchemaSize()
    assert item.short is not None
    assert not item.short
    assert item.with_conn is not None
    assert not item.with_conn


@parametrize_with_cases("key", cases=CaseSchemaSizeAttr)
def test_valid_schema(key: str) -> None:
    d = {key: True}
    item = SchemaSize(**d)
    assert item.__getattribute__(key)


@parametrize_with_cases("key", cases=CaseSchemaSizeAttr)
def test_invalid_schema(key: str) -> None:
    d = {key: None}
    with pytest.raises(ValueError):
        SchemaSize(**d)


def test_default_pagination() -> None:
    item = Pagination()
    assert item.page is not None
    assert item.page == 0
    assert item.size is None


@parametrize_with_cases("key", cases=CasePaginationAttr)
def test_valid_pagination(key: str) -> None:
    d = {key: randint(0 if key == "page" else 1, 100)}
    if key == "page":
        d["size"] = 1
    item = Pagination(**d)
    assert item.__getattribute__(key) == d.get(key)


def test_set_page_to_0() -> None:
    item = Pagination(page=randint(1, 100))
    assert item.size is None
    assert item.page == 0


@parametrize_with_cases("key, value", cases=CasePaginationInvalidAttr)
def test_invalid_pagination(key: str, value: Optional[int]) -> None:
    d = {key: value}
    if key == "page":
        d["size"] = 1
    with pytest.raises(ValueError):
        Pagination(**d)


def test_default_db_params() -> None:
    item = DbQueryCommonParams()
    assert item.skip is not None
    assert item.skip == 0
    assert item.limit is None
    assert item.sort is None


@parametrize_with_cases("key, value", cases=CaseDbQueryAttr)
def test_valid_db_params(key: str, value: Any) -> None:
    d = {key: value}
    item = DbQueryCommonParams(**d)
    assert item.__getattribute__(key) == d.get(key)


@parametrize_with_cases("input, output", cases=CaseSort)
def test_parse_sort(input: str, output: str) -> None:
    item = DbQueryCommonParams(sort=input)
    assert item.sort is not None
    assert item.sort == output


@parametrize_with_cases("key, value", cases=CaseDbQueryInvalidAttr)
def test_invalid_db_params(key: str, value: Optional[int]) -> None:
    d = {key: value}
    with pytest.raises(ValueError):
        DbQueryCommonParams(**d)
