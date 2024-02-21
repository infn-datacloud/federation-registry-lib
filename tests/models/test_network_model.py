from random import randint
from typing import Any, List, Literal, Tuple
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import (
    AttemptedCardinalityViolation,
    CardinalityViolation,
    RelationshipManager,
    RequiredProperty,
)
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.network.models import Network
from fed_reg.project.models import Project
from fed_reg.service.models import NetworkService
from tests.create_dict import network_model_dict
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
    d = network_model_dict()
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
    d = network_model_dict()
    d[missing_attr] = None
    item = Network(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = network_model_dict()
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


@patch("neomodel.match.QueryBuilder._count", return_value=0)
def test_linked_project(
    mock_count: MagicMock,
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    network_model: Network,
    project_model: Project,
) -> None:
    assert network_model.project.name
    assert network_model.project.source
    assert isinstance(network_model.project.source, Network)
    assert network_model.project.source.uid == network_model.uid
    assert network_model.project.definition
    assert network_model.project.definition["node_class"] == Project

    r = network_model.project.connect(project_model)
    assert r is True

    db_match.cypher_query.return_value = ([[project_model]], ["project_r1"])
    assert len(network_model.project.all()) == 1
    project = network_model.project.single()
    assert isinstance(project, Project)
    assert project.uid == project_model.uid


def test_multiple_linked_project(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    network_model: Network,
    project_model: Project,
) -> None:
    with patch("neomodel.match.QueryBuilder._count") as mock_count:
        mock_count.return_value = 1
        with pytest.raises(AttemptedCardinalityViolation):
            network_model.project.connect(project_model)

    db_match.cypher_query.return_value = (
        [[project_model], [project_model]],
        ["project_r1", "project_r2"],
    )
    with pytest.raises(CardinalityViolation):
        network_model.project.all()


@patch("neomodel.match.QueryBuilder._count", return_value=0)
def test_linked_service(
    mock_count: MagicMock,
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    network_model: Network,
    network_service_model: NetworkService,
) -> None:
    assert network_model.service.name
    assert network_model.service.source
    assert isinstance(network_model.service.source, Network)
    assert network_model.service.source.uid == network_model.uid
    assert network_model.service.definition
    assert network_model.service.definition["node_class"] == NetworkService

    r = network_model.service.connect(network_service_model)
    assert r is True

    db_match.cypher_query.return_value = ([[network_service_model]], ["service_r1"])
    assert len(network_model.service.all()) == 1
    service = network_model.service.single()
    assert isinstance(service, NetworkService)
    assert service.uid == network_service_model.uid


def test_multiple_linked_service(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    network_model: Network,
    network_service_model: NetworkService,
) -> None:
    with patch("neomodel.match.QueryBuilder._count") as mock_count:
        mock_count.return_value = 1
        with pytest.raises(AttemptedCardinalityViolation):
            network_model.service.connect(network_service_model)

    db_match.cypher_query.return_value = (
        [[network_service_model], [network_service_model]],
        ["service_r1", "service_r2"],
    )
    with pytest.raises(CardinalityViolation):
        network_model.service.all()
