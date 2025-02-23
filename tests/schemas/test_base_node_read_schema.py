"""Test custom  authentication functions."""

from datetime import date, datetime

import pytest
from neo4j.time import Date
from neomodel import (
    DateProperty,
    DateTimeProperty,
    One,
    OneOrMore,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    ZeroOrMore,
    ZeroOrOne,
)
from neomodel.exceptions import AttemptedCardinalityViolation, CardinalityViolation
from pydantic import Field
from pytest_cases import parametrize_with_cases

from fedreg.core import BaseNodeRead
from tests.utils import random_lower_string


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


class TestORMChild(StructuredNode):
    __test__ = False
    uid = StringProperty(default=random_lower_string())


class TestORMParentOneChild(StructuredNode):
    __test__ = False
    uid = StringProperty(default=random_lower_string())
    one = RelationshipFrom(TestORMChild, "A", cardinality=One)


class TestORMParentOneOrMoreChildren(StructuredNode):
    __test__ = False
    uid = StringProperty(default=random_lower_string())
    one_or_more = RelationshipTo(TestORMChild, "B", cardinality=OneOrMore)


class TestORMParentZeroOrMoreChildren(StructuredNode):
    __test__ = False
    uid = StringProperty(default=random_lower_string())
    zero_or_more = RelationshipTo(TestORMChild, "C", cardinality=ZeroOrMore)


class TestORMParentZeroOrOneChild(StructuredNode):
    __test__ = False
    uid = StringProperty(default=random_lower_string())
    zero_or_one = RelationshipTo(TestORMChild, "D", cardinality=ZeroOrOne)


class TestModelChild(BaseNodeRead):
    __test__ = False


class TestModelParentOneChild(BaseNodeRead):
    __test__ = False
    one: TestModelChild = Field(description="One child")


class TestModelParentOneOrMoreChildren(BaseNodeRead):
    __test__ = False
    one_or_more: list[TestModelChild] = Field(..., description="One or more children")


class TestModelParentZeroOrMoreChildren(BaseNodeRead):
    __test__ = False
    zero_or_more: list[TestModelChild] = Field(..., description="Zero or more children")


class TestModelParentZeroOrOneChild(BaseNodeRead):
    __test__ = False
    zero_or_one: TestModelChild | None = Field(..., description="Zero or one child")


def test_valid_read_schema() -> None:
    assert BaseNodeRead.__config__.validate_assignment
    assert BaseNodeRead.__config__.orm_mode

    s = random_lower_string()
    base_node = BaseNodeRead(uid=s)
    assert base_node.uid is not None
    assert base_node.uid == s


def test_invalid_read_schema() -> None:
    with pytest.raises(ValueError):
        BaseNodeRead()


@parametrize_with_cases("input, output", has_tag="date")
def test_cast_neo4j_date(input: date | Date, output: date) -> None:
    item = TestORMDate(date_test=input).save()
    item = TestModelDate.from_orm(item)
    assert item.date_test is not None
    assert item.date_test == output


@parametrize_with_cases("input, output", has_tag="datetime")
def test_cast_neo4j_datetime(input: date | Date, output: datetime) -> None:
    item = TestORMDateTime(datetime_test=input).save()
    item = TestModelDateTime.from_orm(item)
    assert item.datetime_test is not None
    assert item.datetime_test == output


def test_one_relationship() -> None:
    parent_model = TestORMParentOneChild().save()
    with pytest.raises(CardinalityViolation):
        TestModelParentOneChild.from_orm(parent_model)

    child_model = TestORMChild().save()
    parent_model.one.connect(child_model)
    parent = TestModelParentOneChild.from_orm(parent_model)
    assert parent.one is not None
    assert parent.one.uid == child_model.uid

    child_model = TestORMChild().save()
    with pytest.raises(AttemptedCardinalityViolation):
        parent_model.one.connect(child_model)


def test_one_or_more_relationship() -> None:
    parent_model = TestORMParentOneOrMoreChildren().save()
    with pytest.raises(CardinalityViolation):
        TestModelParentOneOrMoreChildren.from_orm(parent_model)

    child_model1 = TestORMChild().save()
    parent_model.one_or_more.connect(child_model1)
    parent = TestModelParentOneOrMoreChildren.from_orm(parent_model)
    assert parent.one_or_more is not None
    assert isinstance(parent.one_or_more, list)
    assert parent.one_or_more[0].uid == child_model1.uid

    child_model2 = TestORMChild().save()
    parent_model.one_or_more.connect(child_model2)
    parent = TestModelParentOneOrMoreChildren.from_orm(parent_model)
    assert parent.one_or_more is not None
    assert len(parent.one_or_more) == 2
    assert parent.one_or_more[0].uid == child_model1.uid
    assert parent.one_or_more[1].uid == child_model2.uid


def test_zero_or_more_relationship() -> None:
    parent_model = TestORMParentZeroOrMoreChildren().save()
    parent = TestModelParentZeroOrMoreChildren.from_orm(parent_model)
    assert parent.zero_or_more is not None
    assert isinstance(parent.zero_or_more, list)
    assert len(parent.zero_or_more) == 0

    child_model1 = TestORMChild().save()
    parent_model = TestORMParentZeroOrMoreChildren().save()
    parent_model.zero_or_more.connect(child_model1)
    parent = TestModelParentZeroOrMoreChildren.from_orm(parent_model)
    assert parent.zero_or_more is not None
    assert len(parent.zero_or_more) == 1
    assert parent.zero_or_more[0].uid == child_model1.uid

    child_model2 = TestORMChild().save()
    parent_model.zero_or_more.connect(child_model2)
    parent = TestModelParentZeroOrMoreChildren.from_orm(parent_model)
    assert parent.zero_or_more is not None
    assert len(parent.zero_or_more) == 2
    assert parent.zero_or_more[0].uid == child_model1.uid
    assert parent.zero_or_more[1].uid == child_model2.uid


def test_zero_or_one_relationship() -> None:
    parent_model = TestORMParentZeroOrOneChild().save()
    parent = TestModelParentZeroOrOneChild.from_orm(parent_model)
    assert parent.zero_or_one is None

    child_model = TestORMChild().save()
    parent_model.zero_or_one.connect(child_model)
    parent = TestModelParentZeroOrOneChild.from_orm(parent_model)
    assert parent.zero_or_one is not None
    assert parent.zero_or_one.uid == child_model.uid

    child_model = TestORMChild().save()
    with pytest.raises(AttemptedCardinalityViolation):
        parent_model.zero_or_one.connect(child_model)
