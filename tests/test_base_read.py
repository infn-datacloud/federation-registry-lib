"""Test custom  authentication functions."""
from datetime import date, datetime
from typing import Tuple, Union

import pytest
from neo4j.time import Date, DateTime
from neomodel import DateProperty, DateTimeProperty, StringProperty, StructuredNode
from pydantic import Field
from pytest_cases import case, parametrize_with_cases

from fed_reg.models import BaseNodeRead
from tests.common.utils import random_date, random_datetime, random_lower_string


class CaseDates:
    @case(tags=["date"])
    def case_py_date(self) -> Tuple[date, date]:
        d = random_date()
        return d, d

    @case(tags=["date"])
    def case_neo4j_date(self) -> Tuple[date, date]:
        d = random_date()
        return Date(d.year, d.month, d.day), d

    @case(tags=["datetime"])
    def case_py_datetime(self) -> Tuple[datetime, datetime]:
        d = random_datetime()
        return d, d

    @case(tags=["datetime"])
    def case_neo4j_datetime(self) -> Tuple[datetime, datetime]:
        d = random_datetime()
        return DateTime(
            d.year, d.month, d.day, d.hour, d.minute, d.second, tzinfo=d.tzinfo
        ), d


class TestModelDate(BaseNodeRead):
    date_test: date = Field(..., description="A test field for dates")


class TestModelDateTime(BaseNodeRead):
    datetime_test: datetime = Field(..., description="A test field for dates")


class TestORMDate(StructuredNode):
    uid = StringProperty(default=random_lower_string())
    date_test = DateProperty()


class TestORMDateTime(StructuredNode):
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
def test_cast_neo4j_date(input: Union[date, Date], output: date) -> None:
    item = TestORMDate(date_test=input)
    item = TestModelDate.from_orm(item)
    assert item.date_test is not None
    assert item.date_test == output


@parametrize_with_cases("input, output", cases=CaseDates, has_tag=["datetime"])
def test_cast_neo4j_datetime(input: Union[date, Date], output: date) -> None:
    item = TestORMDateTime(datetime_test=input)
    item = TestModelDateTime.from_orm(item)
    assert item.datetime_test is not None
    assert item.datetime_test == output


# TODO test relationships validators
