from random import randint
from typing import Any, List, Literal, Tuple
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.network.models import Network
from tests.create_dict import network_dict
from tests.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["name", "uuid"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(key=["description", "proxy_ip", "proxy_user"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()

    @parametrize(key=["mtu"])
    def case_int(self, key: str) -> Tuple[str, int]:
        return key, randint(0, 100)

    @parametrize(key=["is_shared", "is_router_external", "is_default"])
    def case_bool(self, key: str) -> Tuple[str, Literal[True]]:
        return key, True

    @parametrize(key=["empty", "full"])
    def case_list_str(self, key: str) -> Tuple[str, List[str]]:
        if key == "empty":
            return key, []
        return key, [random_lower_string()]


def test_default_attr() -> None:
    d = network_dict()
    item = Network(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid")
    assert item.is_shared is False
    assert item.is_router_external is False
    assert item.is_default is False
    assert item.mtu is None
    assert item.proxy_ip is None
    assert item.proxy_user is None
    assert item.tags is None
    assert isinstance(item.project, RelationshipManager)
    assert isinstance(item.service, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = network_dict()
    d[missing_attr] = None
    item = Network(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = network_dict()
    d[key] = value

    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = Network(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel(db_match: MagicMock, network_model: Network) -> None:
    db_match.cypher_query.return_value = ([], None)
    with pytest.raises(CardinalityViolation):
        network_model.service.all()
    with pytest.raises(CardinalityViolation):
        network_model.service.single()


def test_optional_rel(db_match: MagicMock, network_model: Network) -> None:
    db_match.cypher_query.return_value = ([], None)
    assert len(network_model.project.all()) == 0
    assert network_model.project.single() is None
