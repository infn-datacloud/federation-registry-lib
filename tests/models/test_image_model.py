from typing import Any, List, Literal, Tuple
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.image.models import Image
from tests.create_dict import image_dict
from tests.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["name", "uuid"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(
        key=[
            "description",
            "os_type",
            "os_distro",
            "os_version",
            "architecture",
            "kernel_id",
        ]
    )
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()

    @parametrize(key=["cuda_support", "gpu_driver", "is_public"])
    def case_bool(self, key: str) -> Tuple[str, Literal[True]]:
        return key, True

    @parametrize(key=["empty", "full"])
    def case_list_str(self, key: str) -> Tuple[str, List[str]]:
        if key == "empty":
            return key, []
        return key, [random_lower_string()]


def test_default_attr() -> None:
    d = image_dict()
    item = Image(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid")
    assert item.is_public is True
    assert item.os_type is None
    assert item.os_distro is None
    assert item.os_version is None
    assert item.architecture is None
    assert item.kernel_id is None
    assert item.cuda_support is False
    assert item.gpu_driver is False
    assert item.tags is None
    assert isinstance(item.projects, RelationshipManager)
    assert isinstance(item.services, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = image_dict()
    d[missing_attr] = None
    item = Image(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = image_dict()
    d[key] = value

    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = Image(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel(db_match: MagicMock, image_model: Image) -> None:
    db_match.cypher_query.return_value = ([], None)
    with pytest.raises(CardinalityViolation):
        image_model.services.all()
    with pytest.raises(CardinalityViolation):
        image_model.services.single()


def test_optional_rel(db_match: MagicMock, image_model: Image) -> None:
    db_match.cypher_query.return_value = ([], None)
    assert len(image_model.projects.all()) == 0
    assert image_model.projects.single() is None
