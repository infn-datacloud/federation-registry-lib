from typing import Any, Tuple
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.project.models import Project
from tests.create_dict import project_dict
from tests.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["name", "uuid"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(key=["description"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()


def test_default_attr() -> None:
    d = project_dict()
    item = Project(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid")
    assert isinstance(item.sla, RelationshipManager)
    assert isinstance(item.provider, RelationshipManager)
    assert isinstance(item.quotas, RelationshipManager)
    assert isinstance(item.private_flavors, RelationshipManager)
    assert isinstance(item.private_images, RelationshipManager)
    assert isinstance(item.private_networks, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = project_dict()
    d[missing_attr] = None
    item = Project(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = project_dict()
    d[key] = value

    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = Project(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel(db_match: MagicMock, project_model: Project) -> None:
    db_match.cypher_query.return_value = ([], None)
    with pytest.raises(CardinalityViolation):
        project_model.provider.all()
    with pytest.raises(CardinalityViolation):
        project_model.provider.single()


def test_optional_rel(db_match: MagicMock, project_model: Project) -> None:
    db_match.cypher_query.return_value = ([], None)
    assert len(project_model.sla.all()) == 0
    assert project_model.sla.single() is None
    assert len(project_model.quotas.all()) == 0
    assert project_model.quotas.single() is None
    assert len(project_model.private_flavors.all()) == 0
    assert project_model.private_flavors.single() is None
    assert len(project_model.private_images.all()) == 0
    assert project_model.private_images.single() is None
    assert len(project_model.private_networks.all()) == 0
    assert project_model.private_networks.single() is None


# TODO test public_flavors
# TODO test public_images
# TODO test public_networks
