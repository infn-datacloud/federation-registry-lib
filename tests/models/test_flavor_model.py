from random import randint
from typing import Any, Literal, Tuple
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from neo4j.graph import Node
from neomodel import CardinalityViolation, RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.flavor.models import Flavor
from fed_reg.project.models import Project
from fed_reg.service.models import ComputeService
from tests.create_dict import flavor_model_dict
from tests.utils import random_lower_string


class CaseMissing:
    @parametrize(value=["name", "uuid"])
    def case_missing(self, value: str) -> str:
        return value


class CaseAttr:
    @parametrize(key=["description", "gpu_model", "gpu_vendor", "local_storage"])
    def case_str(self, key: str) -> Tuple[str, str]:
        return key, random_lower_string()

    @parametrize(key=["disk", "ram", "vcpus", "swap", "ephemeral", "gpus"])
    def case_integer(self, key: str) -> Tuple[str, int]:
        return key, randint(0, 100)

    @parametrize(key=["is_public", "infiniband"])
    def case_bool(self, key: str) -> Tuple[str, Literal[True]]:
        return key, True


def test_default_attr() -> None:
    d = flavor_model_dict()
    item = Flavor(**d)
    assert item.uid is not None
    assert item.description == ""
    assert item.name == d.get("name")
    assert item.uuid == d.get("uuid")
    assert item.disk == 0
    assert item.is_public is True
    assert item.ram == 0
    assert item.vcpus == 0
    assert item.swap == 0
    assert item.ephemeral == 0
    assert item.infiniband is False
    assert item.gpus == 0
    assert item.gpu_model is None
    assert item.gpu_vendor is None
    assert item.local_storage is None
    assert isinstance(item.projects, RelationshipManager)
    assert isinstance(item.services, RelationshipManager)


@parametrize_with_cases("missing_attr", cases=CaseMissing)
def test_missing_attr(missing_attr: str) -> None:
    d = flavor_model_dict()
    d[missing_attr] = None
    item = Flavor(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = flavor_model_dict()
    d[key] = value

    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    db_core.cypher_query.return_value = (
        [[Node(..., element_id=element_id, id_=0, properties=d)]],
        None,
    )

    item = Flavor(**d)
    saved = item.save()

    assert saved.element_id_property == element_id
    assert saved.uid == item.uid
    assert saved.__getattribute__(key) == value


def test_required_rel(db_match: MagicMock, flavor_model: Flavor) -> None:
    db_match.cypher_query.return_value = ([], None)
    with pytest.raises(CardinalityViolation):
        flavor_model.services.all()
    with pytest.raises(CardinalityViolation):
        flavor_model.services.single()


def test_optional_rel(db_match: MagicMock, flavor_model: Flavor) -> None:
    db_match.cypher_query.return_value = ([], None)
    assert len(flavor_model.projects.all()) == 0
    assert flavor_model.projects.single() is None


def test_linked_project(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    flavor_model: Flavor,
    project_model: Project,
) -> None:
    assert flavor_model.projects.name
    assert flavor_model.projects.source
    assert isinstance(flavor_model.projects.source, Flavor)
    assert flavor_model.projects.source.uid == flavor_model.uid
    assert flavor_model.projects.definition
    assert flavor_model.projects.definition["node_class"] == Project

    r = flavor_model.projects.connect(project_model)
    assert r is True

    db_match.cypher_query.return_value = ([[project_model]], ["projects_r1"])
    assert len(flavor_model.projects.all()) == 1
    project = flavor_model.projects.single()
    assert isinstance(project, Project)
    assert project.uid == project_model.uid


def test_multiple_linked_projects(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    flavor_model: Flavor,
    project_model: Project,
) -> None:
    db_match.cypher_query.return_value = (
        [[project_model], [project_model]],
        ["projects_r1", "projects_r2"],
    )
    assert len(flavor_model.projects.all()) == 2


def test_linked_service(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    flavor_model: Flavor,
    compute_service_model: ComputeService,
) -> None:
    assert flavor_model.services.name
    assert flavor_model.services.source
    assert isinstance(flavor_model.services.source, Flavor)
    assert flavor_model.services.source.uid == flavor_model.uid
    assert flavor_model.services.definition
    assert flavor_model.services.definition["node_class"] == ComputeService

    r = flavor_model.services.connect(compute_service_model)
    assert r is True

    db_match.cypher_query.return_value = ([[compute_service_model]], ["services_r1"])
    assert len(flavor_model.services.all()) == 1
    service = flavor_model.services.single()
    assert isinstance(service, ComputeService)
    assert service.uid == compute_service_model.uid


def test_multiple_linked_services(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    flavor_model: Flavor,
    compute_service_model: ComputeService,
) -> None:
    db_match.cypher_query.return_value = (
        [[compute_service_model], [compute_service_model]],
        ["services_r1", "services_r2"],
    )
    assert len(flavor_model.services.all()) == 2
