from typing import Any, List, Literal, Tuple
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from neo4j.graph import Node, Relationship
from neomodel import RelationshipManager, RequiredProperty
from pytest_cases import parametrize, parametrize_with_cases

from fed_reg.auth_method.models import AuthMethod
from fed_reg.identity_provider.models import IdentityProvider
from fed_reg.project.models import Project
from fed_reg.provider.models import Provider
from fed_reg.region.models import Region
from tests.create_dict import auth_method_dict, provider_model_dict
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
    d = provider_model_dict()
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
    d = provider_model_dict()
    d[missing_attr] = None
    item = Provider(**d)
    with pytest.raises(RequiredProperty):
        item.save()


@parametrize_with_cases("key, value", cases=CaseAttr)
def test_attr(db_core: MagicMock, key: str, value: Any) -> None:
    d = provider_model_dict()
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


def test_linked_project(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    provider_model: Provider,
    project_model: Project,
) -> None:
    assert provider_model.projects.name
    assert provider_model.projects.source
    assert isinstance(provider_model.projects.source, Provider)
    assert provider_model.projects.source.uid == provider_model.uid
    assert provider_model.projects.definition
    assert provider_model.projects.definition["node_class"] == Project

    r = provider_model.projects.connect(project_model)
    assert r is True

    db_match.cypher_query.return_value = ([[project_model]], ["projects_r1"])
    assert len(provider_model.projects.all()) == 1
    project = provider_model.projects.single()
    assert isinstance(project, Project)
    assert project.uid == project_model.uid


def test_multiple_linked_projects(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    provider_model: Provider,
    project_model: Project,
) -> None:
    db_match.cypher_query.return_value = (
        [[project_model], [project_model]],
        ["projects_r1", "projects_r2"],
    )
    assert len(provider_model.projects.all()) == 2


def test_linked_region(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    provider_model: Provider,
    region_model: Region,
) -> None:
    assert provider_model.regions.name
    assert provider_model.regions.source
    assert isinstance(provider_model.regions.source, Provider)
    assert provider_model.regions.source.uid == provider_model.uid
    assert provider_model.regions.definition
    assert provider_model.regions.definition["node_class"] == Region

    r = provider_model.regions.connect(region_model)
    assert r is True

    db_match.cypher_query.return_value = ([[region_model]], ["regions_r1"])
    assert len(provider_model.regions.all()) == 1
    region = provider_model.regions.single()
    assert isinstance(region, Region)
    assert region.uid == region_model.uid


def test_multiple_linked_regions(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    provider_model: Provider,
    region_model: Region,
) -> None:
    db_match.cypher_query.return_value = (
        [[region_model], [region_model]],
        ["regions_r1", "regions_r2"],
    )
    assert len(provider_model.regions.all()) == 2


def test_linked_identity_provider(
    db_rel_mgr: MagicMock,
    db_core: MagicMock,
    db_match: MagicMock,
    provider_model: Provider,
    identity_provider_model: IdentityProvider,
) -> None:
    assert provider_model.identity_providers.name
    assert provider_model.identity_providers.source
    assert isinstance(provider_model.identity_providers.source, Provider)
    assert provider_model.identity_providers.source.uid == provider_model.uid
    assert provider_model.identity_providers.definition
    assert (
        provider_model.identity_providers.definition["node_class"] == IdentityProvider
    )

    d = auth_method_dict()
    element_id = f"{db_core.database_version}:{uuid4().hex}:0"
    r = Relationship(..., element_id=element_id, id_=0, properties=d)
    r._start_node = Node(
        ...,
        element_id=provider_model.element_id,
        id_=int(provider_model.element_id[provider_model.element_id.rfind(":") + 1 :]),
    )
    r._end_node = Node(
        ...,
        element_id=identity_provider_model.element_id,
        id_=int(
            identity_provider_model.element_id[
                identity_provider_model.element_id.rfind(":") + 1 :
            ]
        ),
    )
    db_core.cypher_query.return_value = ([[r]], None)
    r = provider_model.identity_providers.connect(identity_provider_model, d)
    assert isinstance(r, AuthMethod)
    assert r.idp_name == d["idp_name"]
    assert r.protocol == d["protocol"]

    db_match.cypher_query.return_value = (
        [[identity_provider_model]],
        ["identity_providers_r1"],
    )
    assert len(provider_model.identity_providers.all()) == 1
    identity_provider = provider_model.identity_providers.single()
    assert isinstance(identity_provider, IdentityProvider)
    assert identity_provider.uid == identity_provider_model.uid


def test_multiple_linked_identity_providers(
    db_rel_mgr: MagicMock,
    db_match: MagicMock,
    provider_model: Provider,
    identity_provider_model: IdentityProvider,
) -> None:
    db_match.cypher_query.return_value = (
        [[identity_provider_model], [identity_provider_model]],
        ["identity_providers_r1", "identity_providers_r2"],
    )
    assert len(provider_model.identity_providers.all()) == 2
