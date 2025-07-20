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
    StructuredRel,
    ZeroOrMore,
    ZeroOrOne,
)
from neomodel.exceptions import AttemptedCardinalityViolation, CardinalityViolation
from pydantic import BaseModel, Field
from pytest_cases import parametrize_with_cases

from fedreg.core import (
    BaseNodeRead,
    BaseReadPrivate,
    BaseReadPrivateExtended,
    BaseReadPublic,
    BaseReadPublicExtended,
)
from tests.utils import random_lower_string


class TestModelDate(BaseNodeRead):
    __test__ = False
    date_test: date = Field(..., description="A test field for dates")


class TestModelDateTime(BaseNodeRead):
    __test__ = False
    datetime_test: datetime = Field(..., description="A test field for dates")


class TestORMDate(StructuredNode):
    __test__ = False
    uid = StringProperty()
    date_test = DateProperty()


class TestORMDateTime(StructuredNode):
    __test__ = False
    uid = StringProperty()
    date_test = DateTimeProperty()


class TestORMRelationship(StructuredRel):
    __test__ = False
    test_field = StringProperty()


class TestORMChild(StructuredNode):
    __test__ = False
    uid = StringProperty()


class TestORMParentOneChild(StructuredNode):
    __test__ = False
    uid = StringProperty()
    one = RelationshipFrom(TestORMChild, "A", cardinality=One)


class TestORMParentOneOrMoreChildren(StructuredNode):
    __test__ = False
    uid = StringProperty()
    one_or_more = RelationshipTo(TestORMChild, "B", cardinality=OneOrMore)


class TestORMParentZeroOrMoreChildren(StructuredNode):
    __test__ = False
    uid = StringProperty()
    zero_or_more = RelationshipTo(TestORMChild, "C", cardinality=ZeroOrMore)


class TestORMParentZeroOrOneChild(StructuredNode):
    __test__ = False
    uid = StringProperty()
    zero_or_one = RelationshipTo(TestORMChild, "D", cardinality=ZeroOrOne)


class TestORMParentChildWithRelationship(StructuredNode):
    __test__ = False
    uid = StringProperty()
    zero_or_one = RelationshipTo(
        TestORMChild, "E", cardinality=ZeroOrOne, model=TestORMRelationship
    )


class TestORMParentChildrenWithRelationship(StructuredNode):
    __test__ = False
    uid = StringProperty()
    zero_or_more = RelationshipTo(
        TestORMChild, "E", cardinality=ZeroOrMore, model=TestORMRelationship
    )


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


class TestModelRelationship(BaseModel):
    __test__ = False
    test_field: str = Field(description="A test field for relationships")

    class Config:
        orm_mode = True


class TestModelChildWithRelationship(BaseNodeRead):
    __test__ = False
    relationship: TestModelRelationship = Field(
        description="A test field for relationships"
    )


class TestModelParentChildWithRelationship(BaseNodeRead):
    __test__ = False
    zero_or_one: TestModelChildWithRelationship | None = Field(description="One child")


class TestModelParentChildrenWithRelationship(BaseNodeRead):
    __test__ = False
    zero_or_more: list[TestModelChildWithRelationship] = Field(description="One child")


class TestModelSchemaTypePublic(BaseNodeRead, BaseReadPublic):
    __test__ = False


class TestModelSchemaTypePrivate(BaseNodeRead, BaseReadPrivate):
    __test__ = False


class TestModelSchemaTypePublicExtended(BaseNodeRead, BaseReadPublicExtended):
    __test__ = False


class TestModelSchemaTypePrivateExtended(BaseNodeRead, BaseReadPrivateExtended):
    __test__ = False


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
    item = TestORMDate(uid=random_lower_string(), date_test=input).save()
    item = TestModelDate.from_orm(item)
    assert item.date_test is not None
    assert item.date_test == output


@parametrize_with_cases("input, output", has_tag="datetime")
def test_cast_neo4j_datetime(input: date | Date, output: datetime) -> None:
    item = TestORMDateTime(uid=random_lower_string(), datetime_test=input).save()
    item = TestModelDateTime.from_orm(item)
    assert item.datetime_test is not None
    assert item.datetime_test == output


def test_one_relationship() -> None:
    parent_model = TestORMParentOneChild(uid=random_lower_string()).save()
    with pytest.raises(CardinalityViolation):
        TestModelParentOneChild.from_orm(parent_model)

    child_model = TestORMChild(uid=random_lower_string()).save()
    parent_model.one.connect(child_model)
    parent = TestModelParentOneChild.from_orm(parent_model)
    assert parent.one is not None
    assert parent.one.uid == child_model.uid

    child_model = TestORMChild(uid=random_lower_string()).save()
    with pytest.raises(AttemptedCardinalityViolation):
        parent_model.one.connect(child_model)


def test_one_or_more_relationship() -> None:
    parent_model = TestORMParentOneOrMoreChildren(uid=random_lower_string()).save()
    with pytest.raises(CardinalityViolation):
        TestModelParentOneOrMoreChildren.from_orm(parent_model)

    child_model1 = TestORMChild(uid=random_lower_string()).save()
    parent_model.one_or_more.connect(child_model1)
    parent = TestModelParentOneOrMoreChildren.from_orm(parent_model)
    assert parent.one_or_more is not None
    assert isinstance(parent.one_or_more, list)
    assert parent.one_or_more[0].uid == child_model1.uid

    child_model2 = TestORMChild(uid=random_lower_string()).save()
    parent_model.one_or_more.connect(child_model2)
    parent = TestModelParentOneOrMoreChildren.from_orm(parent_model)
    assert parent.one_or_more is not None
    assert len(parent.one_or_more) == 2
    # The order of the relationships is not guaranteed
    assert parent.one_or_more[1].uid == child_model1.uid
    assert parent.one_or_more[0].uid == child_model2.uid


def test_zero_or_more_relationship() -> None:
    parent_model = TestORMParentZeroOrMoreChildren(uid=random_lower_string()).save()
    parent = TestModelParentZeroOrMoreChildren.from_orm(parent_model)
    assert parent.zero_or_more is not None
    assert isinstance(parent.zero_or_more, list)
    assert len(parent.zero_or_more) == 0

    child_model1 = TestORMChild(uid=random_lower_string()).save()
    parent_model = TestORMParentZeroOrMoreChildren(uid=random_lower_string()).save()
    parent_model.zero_or_more.connect(child_model1)
    parent = TestModelParentZeroOrMoreChildren.from_orm(parent_model)
    assert parent.zero_or_more is not None
    assert len(parent.zero_or_more) == 1
    assert parent.zero_or_more[0].uid == child_model1.uid

    child_model2 = TestORMChild(uid=random_lower_string()).save()
    parent_model.zero_or_more.connect(child_model2)
    parent = TestModelParentZeroOrMoreChildren.from_orm(parent_model)
    assert parent.zero_or_more is not None
    assert len(parent.zero_or_more) == 2
    # The order of the relationships is not guaranteed
    assert parent.zero_or_more[1].uid == child_model1.uid
    assert parent.zero_or_more[0].uid == child_model2.uid


def test_zero_or_one_relationship() -> None:
    parent_model = TestORMParentZeroOrOneChild(uid=random_lower_string()).save()
    parent = TestModelParentZeroOrOneChild.from_orm(parent_model)
    assert parent.zero_or_one is None

    child_model = TestORMChild(uid=random_lower_string()).save()
    parent_model.zero_or_one.connect(child_model)
    parent = TestModelParentZeroOrOneChild.from_orm(parent_model)
    assert parent.zero_or_one is not None
    assert parent.zero_or_one.uid == child_model.uid

    child_model = TestORMChild(uid=random_lower_string()).save()
    with pytest.raises(AttemptedCardinalityViolation):
        parent_model.zero_or_one.connect(child_model)


def test_zero_or_one_rel_with_data() -> None:
    parent_model = TestORMParentChildWithRelationship(uid=random_lower_string()).save()
    parent = TestModelParentChildWithRelationship.from_orm(parent_model)
    assert parent.zero_or_one is None

    child_model = TestORMChild(uid=random_lower_string()).save()
    parent_model.zero_or_one.connect(child_model, {"test_field": "test"})
    parent = TestModelParentChildWithRelationship.from_orm(parent_model)
    assert parent.zero_or_one is not None
    assert parent.zero_or_one.uid == child_model.uid
    assert parent.zero_or_one.relationship.test_field == "test"


def test_zero_or_more_rel_with_data() -> None:
    parent_model = TestORMParentChildrenWithRelationship(
        uid=random_lower_string()
    ).save()
    parent = TestModelParentChildrenWithRelationship.from_orm(parent_model)
    assert parent.zero_or_more is not None
    assert isinstance(parent.zero_or_more, list)
    assert len(parent.zero_or_more) == 0

    child_model1 = TestORMChild(uid=random_lower_string()).save()
    parent_model.zero_or_more.connect(child_model1, {"test_field": "test1"})
    parent = TestModelParentChildrenWithRelationship.from_orm(parent_model)
    assert parent.zero_or_more is not None
    assert len(parent.zero_or_more) == 1
    assert parent.zero_or_more[0].uid == child_model1.uid
    assert parent.zero_or_more[0].relationship.test_field == "test1"

    child_model2 = TestORMChild(uid=random_lower_string()).save()
    parent_model.zero_or_more.connect(child_model2, {"test_field": "test2"})
    parent = TestModelParentChildrenWithRelationship.from_orm(parent_model)
    assert parent.zero_or_more is not None
    assert len(parent.zero_or_more) == 2
    # The order of the relationships is not guaranteed
    assert parent.zero_or_more[1].uid == child_model1.uid
    assert parent.zero_or_more[1].relationship.test_field == "test1"
    assert parent.zero_or_more[0].uid == child_model2.uid
    assert parent.zero_or_more[0].relationship.test_field == "test2"


def test_schema_type_public() -> None:
    item = TestModelSchemaTypePublic(uid=random_lower_string())
    assert item.schema_type == "public"


def test_schema_type_private() -> None:
    item = TestModelSchemaTypePrivate(uid=random_lower_string())
    assert item.schema_type == "private"


def test_schema_type_public_extended() -> None:
    item = TestModelSchemaTypePublicExtended(uid=random_lower_string())
    assert item.schema_type == "public_extended"


def test_schema_type_private_extended() -> None:
    item = TestModelSchemaTypePrivateExtended(uid=random_lower_string())
    assert item.schema_type == "private_extended"
