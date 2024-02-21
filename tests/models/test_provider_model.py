from typing import Any, List, Literal, Tuple
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.provider.models import Provider
from tests.create_dict import provider_dict
from tests.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["name", "type"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(key=["description", "status"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()

    @parametrize(key=["is_public"])
    def case_bool(self, key: str) -> Tuple[str, Literal[True]]:
        return key, True

    @parametrize(key=["empty", "full"])
    def case_list_str(self, key: str) -> Tuple[str, List[str]]:
        if key == "empty":
            return key, []
        return key, [random_lower_string()]


def test_default_attr() -> None:
    d = provider_dict()
    item = Provider(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert item.type == d.get("type")
    assert item.is_public is False
    assert item.status is None
    assert item.support_emails is None
    assert isinstance(item.projects, RelationshipManager)
    assert isinstance(item.regions, RelationshipManager)
    assert isinstance(item.identity_providers, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = provider_dict()
    d[missing_attr] = None
    item = Provider(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = provider_dict()
    d[key] = value

    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = Provider(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_optional_rel(db_match: MagicMock, provider_model: Provider) -> None:
    db_match.cypher_query.return_value = ([], None)
    assert len(provider_model.identity_providers.all()) == 0
    assert provider_model.identity_providers.single() is None
    assert len(provider_model.projects.all()) == 0
    assert provider_model.projects.single() is None
    assert len(provider_model.regions.all()) == 0
    assert provider_model.regions.single() is None
