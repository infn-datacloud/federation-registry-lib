"""Test custom  authentication functions."""
from datetime import date, datetime

import pytest
from neo4j.time import Date, DateTime
from neomodel import DateProperty, DateTimeProperty, StringProperty, StructuredNode
from pydantic import Field
from pytest_cases import case, parametrize_with_cases

from fed_reg.models import BaseNodeRead
from tests.utils import random_date, random_datetime, random_lower_string


class CaseDates:
    @case(tags=["date"])
    def case_py_date(self) -> tuple[date, date]:
        d = random_date()
        return d, d

    @case(tags=["date"])
    def case_neo4j_date(self) -> tuple[date, date]:
        d = random_date()
        return Date(d.year, d.month, d.day), d

    @case(tags=["datetime"])
    def case_py_datetime(self) -> tuple[datetime, datetime]:
        d = random_datetime()
        return d, d

    @case(tags=["datetime"])
    def case_neo4j_datetime(self) -> tuple[datetime, datetime]:
        d = random_datetime()
        return DateTime(
            d.year, d.month, d.day, d.hour, d.minute, d.second, tzinfo=d.tzinfo
        ), d


class TestModelDate(BaseNodeRead):
    __test__ = False
    date_test: date = Field(..., description="A test field for dates")


class TestModelDateTime(BaseNodeRead):
    __test__ = False
    datetime_test: datetime = Field(..., description="A test field for dates")


class TestORMDate(StructuredNode):
    __test__ = False
    uid = StringProperty(default=random_lower_string())
    date_test = DateProperty()


class TestORMDateTime(StructuredNode):
    __test__ = False
    uid = StringProperty(default=random_lower_string())
    date_test = DateTimeProperty()


def test_valid_read_schema() -> None:
    assert BaseNodeRead.__config__.orm_mode

    s = random_lower_string()
    base_node = BaseNodeRead(uid=s)
    assert base_node.uid is not None
    assert base_node.uid == s


def test_invalid_read_schema() -> None:
    with pytest.raises(ValueError):
        BaseNodeRead()


@parametrize_with_cases("input, output", cases=CaseDates, has_tag=["date"])
def test_cast_neo4j_date(input: date | Date, output: date) -> None:
    item = TestORMDate(date_test=input)
    item = TestModelDate.from_orm(item)
    assert item.date_test is not None
    assert item.date_test == output


@parametrize_with_cases("input, output", cases=CaseDates, has_tag=["datetime"])
def test_cast_neo4j_datetime(input: date | Date, output: date) -> None:
    item = TestORMDateTime(datetime_test=input)
    item = TestModelDateTime.from_orm(item)
    assert item.datetime_test is not None
    assert item.datetime_test == output


# TODO test relationships validators
