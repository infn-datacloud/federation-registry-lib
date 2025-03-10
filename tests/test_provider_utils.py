import pytest
from pydantic import BaseModel, Field

from fedreg.provider.utils import find_duplicates, multiple_quotas_same_project
from fedreg.quota.schemas import QuotaBase


class TestModel(BaseModel):
    __test__ = False
    test_field: str = Field(decription="Test field")


class TestQuota(QuotaBase):
    __test__ = False
    project: str = Field(description="Project field")


def test_find_duplicates() -> None:
    a = "str1"
    b = "str2"
    find_duplicates([a, b])

    a = "str1"
    b = "str1"
    with pytest.raises(
        AssertionError, match=f"There are multiple identical items: {a}"
    ):
        find_duplicates([a, b])

    a = TestModel(test_field="str1")
    b = TestModel(test_field="str2")
    find_duplicates([a, b], attr="test_field")

    a = TestModel(test_field="str1")
    b = TestModel(test_field="str1")
    with pytest.raises(
        AssertionError,
        match=f"There are multiple items with identical test_field: {a.test_field}",
    ):
        find_duplicates([a, b], attr="test_field")


def test_multiple_quotas() -> None:
    project = "project1"
    q1 = TestQuota(project=project)
    multiple_quotas_same_project([q1])
    q2 = TestQuota(project=project, per_user=True)
    multiple_quotas_same_project([q1, q2])
    q3 = TestQuota(project=project, usage=True)
    multiple_quotas_same_project([q1, q2, q3])

    q4 = TestQuota(project="project2")
    multiple_quotas_same_project([q1, q2, q4])
    q4 = TestQuota(project="project2", per_user=True)
    multiple_quotas_same_project([q1, q2, q4])
    q4 = TestQuota(project="project2", usage=True)
    multiple_quotas_same_project([q1, q2, q4])

    q4 = TestQuota(project=project)
    with pytest.raises(
        AssertionError, match=f"Multiple quotas on same project {project}"
    ):
        multiple_quotas_same_project([q1, q2, q3, q4])

    q4 = TestQuota(project=project, per_user=True)
    with pytest.raises(
        AssertionError, match=f"Multiple quotas on same project {project}"
    ):
        multiple_quotas_same_project([q1, q2, q3, q4])

    q4 = TestQuota(project=project, usage=True)
    with pytest.raises(
        AssertionError, match=f"Multiple quotas on same project {project}"
    ):
        multiple_quotas_same_project([q1, q2, q3, q4])
